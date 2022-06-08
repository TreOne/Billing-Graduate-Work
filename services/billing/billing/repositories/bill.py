from typing import List, Optional, Tuple

from rest_framework.exceptions import NotFound
from rest_framework.request import Request

from api.v1.bills.serializers import BillCreateRequestSerializer, BillCreateSerializer
from billing.models import Bill
from billing.models.enums import BillType
from billing.repositories.base import BaseRepository
from billing.repositories.movie import MovieRepository
from billing.repositories.role import RoleRepository

__all__ = ("BillRepository",)

from billing.repositories.user_autopay import UserAutoPayRepository
from config.payment_service import payment_system
from utils.schemas import PaymentParams


class BillRepository(BaseRepository):

    MODEL_CLASS = Bill

    @classmethod
    def get_user_bills(cls, user_uuid: str) -> List[Bill]:
        return cls.MODEL_CLASS.objects.filter(user_uuid=user_uuid)

    @classmethod
    def buy_item(cls, request: Request) -> dict:
        user_uuid: str = request.user.id
        autopay_id: Optional[str] = UserAutoPayRepository.get_users_auto_pay(
            user_uuid=user_uuid
        )
        if autopay_id:
            result: dict = cls._buy_item_with_autopay(
                user_uuid=user_uuid,
                autopay_id=autopay_id,
                request=request,
            )
        else:
            confirmation_url = cls._buy_item_without_autopay(
                user_uuid=user_uuid,
                request=request,
            )
            result: dict = {"confirmation_url": confirmation_url}
        return result

    @classmethod
    def _buy_item_with_autopay(
        cls, user_uuid: str, autopay_id: str, request: Request
    ) -> dict:
        """Оплата с сохраненным токеном."""

        item_uuid, bill_type = cls._validate_request(request=request)

        description, amount = cls._determine_data_by_bill_type(
            bill_type=bill_type,
            item_uuid=item_uuid,
        )

        bill_uuid: str = cls._create_bill(
            request=request,
            user_uuid=user_uuid,
            amount=amount,
        )

        auto_payment_params = PaymentParams(
            bill_uuid=bill_uuid,
            user_uuid=user_uuid,
            amount=amount,
            description=description,
            autopay_id=autopay_id,
        )
        is_successful = payment_system.make_autopay(auto_payment_params)
        if is_successful:
            message: str = "Автоплатеж проведен успешно."
        else:
            message: str = "ОШИБКА: Не удалось выполнить автоплатеж!"
        return {"message": message, "is_successful": is_successful}

    @classmethod
    def _buy_item_without_autopay(cls, user_uuid: str, request: Request) -> str:
        """Оплата без сохраненного токена."""

        item_uuid, bill_type = cls._validate_request(request=request)

        description, amount = cls._determine_data_by_bill_type(
            bill_type=bill_type,
            item_uuid=item_uuid,
        )

        bill_uuid: str = cls._create_bill(
            request=request,
            user_uuid=user_uuid,
            amount=amount,
        )

        payment_params = PaymentParams(
            bill_uuid=bill_uuid,
            user_uuid=user_uuid,
            amount=amount,
            description=description,
            save_payment_method=True,
        )
        confirmation_url: str = payment_system.create_confirmation_url(
            params=payment_params
        )
        return confirmation_url

    @classmethod
    def _validate_request(cls, request: Request) -> Tuple[str, str]:
        request_serializer = BillCreateRequestSerializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)
        request_serializer = request_serializer.save()
        item_uuid: str = request_serializer.get("item_uuid")
        bill_type: str = request_serializer.get("type")
        return item_uuid, bill_type

    @classmethod
    def _determine_data_by_bill_type(
        cls, bill_type: str, item_uuid: str
    ) -> Tuple[str, float]:
        """Возвращает данные для оплаты в зависимости от типа оплаты."""
        if bill_type == BillType.movie:
            movie_title, amount = MovieRepository.get_by_id(item_uuid=item_uuid)
            description: str = f"У вас теперь есть фильм '{movie_title}'."
            return description, amount
        elif bill_type == BillType.subscription:
            role = RoleRepository.get_by_id(item_uuid=item_uuid)
            amount = role.get("price")
            description: str = f"У вас теперь есть роль '{role.get('title_ru')}'."
            return description, amount
        else:
            raise NotFound

    @classmethod
    def _create_bill(cls, request: Request, user_uuid: str, amount: float) -> str:
        """Создаем в БД объект оплаты"""
        serializer = BillCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        bill = serializer.save(user_uuid=user_uuid, amount=amount)
        bill_uuid: str = str(bill.id)
        return bill_uuid
