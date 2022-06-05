from typing import List

from billing.models import Bill
from billing.repositories import BaseRepository

__all__ = ("BillRepository",)


class BillRepository(BaseRepository):

    MODEL_CLASS = Bill

    @classmethod
    def get_user_bills(cls, user_uuid: str) -> List[Bill]:
        return cls.MODEL_CLASS.objects.filter(user_uuid=user_uuid)
