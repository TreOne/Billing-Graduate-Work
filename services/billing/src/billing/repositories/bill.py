import logging
from typing import List, NamedTuple, TypedDict, Union

from rest_framework.exceptions import ValidationError

from billing.models import Bill
from billing.models.enums import BillType
from billing.repositories.base import BaseRepository
from billing.repositories.movie import MovieRepository
from billing.repositories.role import RoleRepository

__all__ = ('BillRepository',)

from billing.repositories.user_autopay import UserAutoPayRepository
from config.payment_service import payment_system
from utils.schemas import BillBaseSchema, PaymentParams

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
        return cls.MODEL_CLASS.objects.filter(user_uuid=user_uuid)

    @classmethod
    def refund_bill(cls, bill_uuid: str) -> None:
        bill: Bill = cls.get_by_id(item_uuid=bill_uuid)
        logger.info(f'Refund bill with {bill_uuid=}. Payment {bill.payment_uuid=} & {bill.amount=}')
        payment_system.refund_payment(
            payment_id=bill.payment_uuid,
            amount=bill.amount,
        )

    @classmethod
    def determine_bill_status(cls, bill_status: str) -> str:
        """Определить статус Оплаты."""
        return payment_system.convert_bill_status(bill_status)

    @classmethod
    def update_bill_status(cls, bill_uuid: str, bill_payment_id: str, bill_status: str) -> None:
        """Обновление статуса Оплаты."""
        bill = cls.MODEL_CLASS.objects.get(id=bill_uuid)
        logger.info(f'Bill [{bill_uuid=}] status update to "{bill_status}".')
        bill.status = bill_status
        bill.payment_uuid = bill_payment_id
        bill.save()

    @classmethod
    def resave_refund(cls, bill_payment_id: str, refund_payment_id: str, bill_status: str) -> None:
        """Обновление статуса Оплаты."""
        bill = cls.MODEL_CLASS.objects.filter(payment_uuid=bill_payment_id).first()
        logger.info(
            f'Bill [{bill.id=}] status update to "{bill_status}".'
            f'Payment id update from "{bill.payment_uuid}" to "{bill_payment_id}"'
        )
        bill.status = bill_status
        bill.payment_uuid = refund_payment_id
        bill.save()

    @classmethod
    def buy_item(
        cls, bill_schema: BillBaseSchema
    ) -> tuple[Union[AutoPayResult, NotAutoPayResult], bool]:
        """Оплата Подписки или фильма."""
        user_uuid: str = bill_schema.user_uuid
        autopay = UserAutoPayRepository.get_users_auto_pay(user_uuid=user_uuid)
        if autopay:
            is_auto_paid: bool = True
            logger.info('User paid via auto payment.', extra=bill_schema.dict())
            result = cls.buy_item_with_autopay(
                bill_schema=bill_schema, autopay_id=str(autopay.id)
            )
            return result, is_auto_paid
        else:
            is_auto_paid: bool = False
            logger.info('The user paid through a link to Yookassa.', extra=bill_schema.dict())
            confirmation_url: str = cls.buy_item_without_autopay(bill_schema)
            result = NotAutoPayResult(**{'confirmation_url': confirmation_url})
            return result, is_auto_paid

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

        return BillItemData(description=description, amount=amount)

    @classmethod
    def _create_bill(cls, bill_schema: BillBaseSchema, amount: float) -> str:
        """Создаем в БД объект оплаты"""
        data: dict = bill_schema.dict()
        if (
            cls.MODEL_CLASS.objects.filter(**data).exists()
            and bill_schema.type == BillType.movie
        ):
            logger.info('The user tries to re-purchase the movie.', extra=data)
            raise ValidationError({'detail': 'You have already bought this movie.'})
        new_bill = cls.MODEL_CLASS.objects.create(**{'amount': amount, **data})
        bill_uuid: str = str(new_bill.id)
        return bill_uuid
