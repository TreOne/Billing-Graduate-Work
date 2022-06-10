from abc import abstractmethod, ABC

from pydantic import BaseModel


class Notification(BaseModel):
    """Исходящее сообщение."""

    recipient: str
    subject: str
    body: str
    immediately: bool = False
    log_it: bool = False
    ttl: int = 60 * 60 * 24


class AbstractNotificationService(ABC):
    """Интерфейс отправки уведомлений."""

    @abstractmethod
    def send(self, notification: Notification) -> bool:
        """Отправляет уведомление, возвращает успешность отправки."""
        raise NotImplementedError
