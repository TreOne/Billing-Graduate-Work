from typing import Optional

from billing.models import UserAutoPay
from billing.repositories.base import BaseRepository

__all__ = ("UserAutoPayRepository",)


class UserAutoPayRepository(BaseRepository):
    """Репозиторий по работе с Автоплатежами Пользователя."""

    MODEL_CLASS = UserAutoPay

    @classmethod
    def save_users_auto_pay(cls, payment_id: str, user_uuid: str) -> UserAutoPay:
        """Сохранить автоплатеж."""
        auto_pay = cls.MODEL_CLASS.objects.filter(user_uuid=user_uuid)
        if not auto_pay.first():
            auto_pay = auto_pay.create(id=payment_id, user_uuid=user_uuid)
        return auto_pay

    @classmethod
    def get_users_auto_pay(cls, user_uuid: str) -> Optional[str]:
        """Получить автоплатеж конкретного пользователя."""
        try:
            auto_pay_id: str = cls.MODEL_CLASS.objects.get(user_uuid=user_uuid).id
            return str(auto_pay_id)
        except Exception:
            return None
