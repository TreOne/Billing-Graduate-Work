from abc import abstractmethod, ABC
from dataclasses import dataclass
from typing import Optional


@dataclass
class UserSchema:
    """Represents incoming user model."""
    email: str
    username: str


class AbstractAuth(ABC):
    """Интерфейс подключения к сервису аутентификации."""

    @abstractmethod
    def get_user_info(self, user_uuid: str) -> Optional[UserSchema]:
        raise NotImplementedError
