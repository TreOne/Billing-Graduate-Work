from typing import Callable

from services.auth_api.base import AbstractAuth
from services.notification_api.base import AbstractNotificationService


class MessageHandler:
    def __init__(self, user_auth_service: AbstractAuth, notification_service: AbstractNotificationService):
        self.__observers: dict[str, list[Callable]] = dict()
        self.user_auth_service = user_auth_service
        self.notification_service = notification_service

    def register(self, title: str, handler: Callable) -> None:
        handlers = self.__observers.setdefault(title, [])
        handlers.append(handler)

    def handle(self, title: str, message: str) -> None:
        handlers = self.__observers.get(title, [])
        for handler in handlers:
            handler(
                message=message,
                user_auth_service=self.user_auth_service,
                notification_service=self.notification_service
            )
