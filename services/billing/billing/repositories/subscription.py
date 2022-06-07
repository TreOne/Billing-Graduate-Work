from typing import Optional

from rest_framework.exceptions import NotFound

from utils import contants

__all__ = ("SubscriptionRepository",)


class SubscriptionRepository:

    MODEL_CLASS = contants.SYSTEM_ROLES

    @classmethod
    def get_by_id(cls, item_uuid: str) -> Optional[dict]:
        try:
            subscription = [
                role for role in cls.MODEL_CLASS if role.get("uuid") == item_uuid
            ][0]
            return subscription
        except Exception:
            raise NotFound
