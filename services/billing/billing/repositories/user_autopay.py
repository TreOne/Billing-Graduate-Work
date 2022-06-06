from typing import List, Optional

from billing.models import UserAutoPay
from billing.repositories import BaseRepository, BillRepository

__all__ = ("UserAutoPayRepository",)


class UserAutoPayRepository(BaseRepository):

    MODEL_CLASS = UserAutoPay

    @classmethod
    def save_users_auto_pay(cls, payment_id: str, bill_uuid: str) -> UserAutoPay:
        bill = BillRepository.get_by_id(item_uuid=bill_uuid)

        auto_pay = cls.MODEL_CLASS()
        auto_pay.id = payment_id
        auto_pay.user_uuid = bill.user_uuid
        auto_pay.save()
        return auto_pay

    @classmethod
    def get_users_auto_pay(cls, user_uuid: str) -> Optional[str]:
        try:
            auto_pay_id: str = cls.MODEL_CLASS.objects.get(user_uuid=user_uuid).id
            return auto_pay_id
        except Exception:
            return None

    @classmethod
    def get_actual_auto_pays(cls, users: List[str]) -> List[UserAutoPay]:
        auto_pays = cls.MODEL_CLASS.objects.filter(user_uuid__in=users)
        return auto_pays

