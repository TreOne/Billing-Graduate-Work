from typing import Callable

from core.settings import Settings
from services.auth_api.base import AbstractAuth
from services.notification_api.base import AbstractNotificationService


class MessageHandler:
    def __init__(
            self,
            user_auth_service: AbstractAuth,
            notification_service: AbstractNotificationService,
            settings: Settings,
    ):
        self.__observers: dict[str, list[Callable]] = dict()
        self.user_auth_service = user_auth_service
        self.notification_service = notification_service
        self.settings = settings

    def register(self, title: str, handler: Callable) -> None:
        handlers = self.__observers.setdefault(title, [])
        handlers.append(handler)

    def handle(self, title: str, message: str) -> None:
        handlers = self.__observers.get(title, [])
        for handler in handlers:
            handler(
                settings=self.settings,
                message=message,
                user_auth_service=self.user_auth_service,
                notification_service=self.notification_service,
            )
