from datetime import datetime
from typing import Optional

from dateutil.relativedelta import relativedelta
from django.utils.timezone import make_aware

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
        auto_pay.bill_uuid = bill_uuid
        auto_pay.save()
        return auto_pay

    @classmethod
    def get_users_auto_pay(cls, user_uuid: str) -> Optional[str]:
        try:
            current_time: datetime = datetime.now()
            month_ago: datetime = current_time - relativedelta(months=1)
            auto_pay_id: str = cls.MODEL_CLASS.objects.filter(
                user_uuid=user_uuid,
                created_at__gte=make_aware(month_ago),
            ).first().id
            return auto_pay_id
        except Exception:
            return None

    @classmethod
    def get_actual_auto_pays(cls):
        ...

