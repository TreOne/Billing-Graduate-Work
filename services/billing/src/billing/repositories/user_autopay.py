import logging
from typing import Optional

from billing.models import UserAutoPay
from billing.repositories.base import BaseRepository

logger = logging.getLogger('billing')

__all__ = ('UserAutoPayRepository',)


class UserAutoPayRepository(BaseRepository):
    """Репозиторий по работе с Автоплатежами Пользователя."""

    MODEL_CLASS = UserAutoPay

    @classmethod
    def save_users_auto_pay(cls, payment_id: str, user_uuid: str) -> None:
        """Сохранить автоплатеж."""
        auto_pay = cls.MODEL_CLASS.objects.filter(user_uuid=user_uuid)
        if not auto_pay.first():
            logger.info(
                'User auto payment saved.',
                extra={'payment': payment_id, 'user': user_uuid},
            )
            auto_pay.create(id=payment_id, user_uuid=user_uuid)

    @classmethod
    def get_users_auto_pay(cls, user_uuid: str) -> Optional[UserAutoPay]:
        """Получить автоплатеж конкретного пользователя."""
        return cls.MODEL_CLASS.objects.filter(user_uuid=user_uuid).first()
