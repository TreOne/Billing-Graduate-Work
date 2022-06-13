import logging
from typing import List, NamedTuple, TypedDict, Union

from rest_framework.exceptions import ValidationError

from api.v1.bills.serializers import BillCreateSerializer
from billing.models import Bill
from billing.models.enums import BillType
from billing.repositories.base import BaseRepository
from billing.repositories.movie import MovieRepository
from billing.repositories.role import RoleRepository

__all__ = ('BillRepository',)

from billing.repositories.user_autopay import UserAutoPayRepository
from config.payment_service import payment_system
from utils.schemas import PaymentParams
from utils.schemas.bill import BillBaseSchema

logger = logging.getLogger('billing')


class BillItemData(NamedTuple):
    """Данные для создания Оплаты."""

    description: str
    amount: float


class AutoPayResult(TypedDict):
    """Результат покупки при оплате сохраненным токеном."""

    message: str
    is_successful: bool


class NotAutoPayResult(TypedDict):
    """Результат покупки при оплате без токена."""

    confirmation_url: str


class BillRepository(BaseRepository):
    """Репозиторий по работе с Оплатами."""

    MODEL_CLASS = Bill

    @classmethod
    def get_user_bills(cls, user_uuid: str) -> List[Bill]:
        """Выдача оплат определенного пользователя."""
        logger.info(f'User {user_uuid} asked for a list of bills.')
        return cls.MODEL_CLASS.objects.filter(user_uuid=user_uuid)

    @classmethod
    def determine_bill_status(cls, bill_status: str) -> str:
        """Определить статус Оплаты."""
        return payment_system.convert_bill_status(bill_status)

    @classmethod
    def update_bill_status(cls, bill_uuid: str, bill_status: str) -> None:
        """Обновление статуса Оплаты."""
        bill = cls.MODEL_CLASS.objects.filter(id=bill_uuid).exclude(status=bill_status)
        logger.info('Notice from YooKassa.')
        if bill:
            logger.info(
                f'Status update to "{bill_status}" for bill => {bill_uuid}.',
                extra={'bill_uuid': bill_uuid, 'bill_status': bill_status},
            )
            bill.update(status=bill_status)

    @classmethod
    def buy_item(cls, bill_schema: BillBaseSchema) -> Union[AutoPayResult, NotAutoPayResult]:
        """Оплата Подписки или фильма."""
        user_uuid: str = bill_schema.user_uuid
        autopay = UserAutoPayRepository.get_users_auto_pay(user_uuid=user_uuid)
        if autopay:
            logger.info('User paid via auto payment.', extra=bill_schema.dict())
            return cls.buy_item_with_autopay(
                bill_schema=bill_schema, autopay_id=str(autopay.id)
            )
        else:
            logger.info(
                'The user paid through a link to Yookassa.', extra=bill_schema.dict()
            )
            confirmation_url: str = cls.buy_item_without_autopay(bill_schema)
            return NotAutoPayResult(**{'confirmation_url': confirmation_url})

    @classmethod
    def buy_item_with_autopay(
        cls, bill_schema: BillBaseSchema, autopay_id: str
    ) -> AutoPayResult:
        """Оплата с сохраненным токеном."""
        description, amount = cls._determine_data_by_bill_type(bill_schema=bill_schema)
        bill_uuid: str = cls._create_bill(bill_schema=bill_schema, amount=amount)

        auto_payment_params = PaymentParams(
            bill_uuid=bill_uuid,
            user_uuid=bill_schema.user_uuid,
            amount=amount,
            description=description,
            autopay_id=autopay_id,
        )
        is_successful: bool = payment_system.make_autopay(params=auto_payment_params)
        if is_successful:
            message: str = 'Auto payment completed successfully.'
        else:
            message: str = 'ERROR: Failed to complete auto payment!'
        logger.info(message, extra=bill_schema.dict())
        return AutoPayResult(**{'message': message, 'is_successful': is_successful})

    @classmethod
    def buy_item_without_autopay(cls, bill_schema: BillBaseSchema) -> str:
        """Оплата без сохраненного токена."""
        description, amount = cls._determine_data_by_bill_type(bill_schema=bill_schema)
        bill_uuid: str = cls._create_bill(bill_schema=bill_schema, amount=amount)

        payment_params = PaymentParams(
            bill_uuid=bill_uuid,
            user_uuid=bill_schema.user_uuid,
            amount=amount,
            description=description,
            save_payment_method=True,
        )
        return payment_system.create_confirmation_url(params=payment_params)

    @classmethod
    def _determine_data_by_bill_type(cls, bill_schema: BillBaseSchema) -> BillItemData:
        """Возвращает данные для оплаты в зависимости от типа оплаты."""
        if bill_schema.type == BillType.movie:
            movie_title, amount = MovieRepository.get_by_id(item_uuid=bill_schema.item_uuid)
            description: str = f"Movie payment '{movie_title}'."
        elif bill_schema.type == BillType.subscription:
            role = RoleRepository.get_by_id(item_uuid=bill_schema.item_uuid)
            amount: float = role.get('price')
            description: str = f"Subscription payment '{role.get('title_ru')}'."
        else:
            message: str = 'Invalid bill type, select "movie" or "subscription".'
            logger.info(message, extra=bill_schema.dict())
            raise ValidationError({'detail': message})

        logger.info(f'{description}. Amount: {amount}.', extra=bill_schema.dict())
        return BillItemData(description=description, amount=amount)

    @classmethod
    def _create_bill(cls, bill_schema: BillBaseSchema, amount: float) -> str:
        """Создаем в БД объект оплаты"""
        user_uuid: str = bill_schema.user_uuid
        serializer = BillCreateSerializer(
            data=bill_schema.dict(), context={'user_uuid': user_uuid}
        )
        serializer.is_valid(raise_exception=True)
        bill = serializer.save(user_uuid=user_uuid, amount=amount)
        bill_uuid: str = str(bill.id)
        return bill_uuid
