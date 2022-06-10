from typing import Optional

from rest_framework.exceptions import NotFound

from utils import constants

__all__ = ("RoleRepository",)


class RoleRepository:
    """Репозиторий по работе с Подписками."""

    MODEL_CLASS = constants.SYSTEM_ROLES

    @classmethod
    def get_by_id(cls, item_uuid: str) -> Optional[dict]:
        try:
            role: dict = [
                role for role in cls.MODEL_CLASS if role.get("uuid") == item_uuid
            ][0]
            return role
        except Exception:
            raise NotFound
