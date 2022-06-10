from abc import ABC, abstractmethod
from typing import Optional

from utils.schemas.user_subscribe import UserSubscribeSchema


class AbstractAuth(ABC):
    """Интерфейс подключения к сервису аутентификации."""

    @abstractmethod
    def get_user_subscriptions_end(self, days: int) -> Optional[UserSubscribeSchema]:
        raise NotImplementedError
