from utils import contants
from typing import Optional

__all__ = ('SubscriptionRepository',)


class SubscriptionRepository:

    MODEL_CLASS = contants.SYSTEM_ROLES

    @classmethod
    def get_by_id(cls, item_uuid: str) -> Optional[dict]:
        return cls.MODEL_CLASS.get(str(item_uuid))
