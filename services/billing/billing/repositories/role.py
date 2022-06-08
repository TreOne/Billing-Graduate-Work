from typing import Optional

from rest_framework.exceptions import NotFound

from utils import contants

__all__ = ("RoleRepository",)


class RoleRepository:

    MODEL_CLASS = contants.SYSTEM_ROLES

    @classmethod
    def get_by_id(cls, item_uuid: str) -> Optional[dict]:
        try:
            role = [role for role in cls.MODEL_CLASS if role.get("uuid") == item_uuid][
                0
            ]
            return role
        except Exception:
            raise NotFound
