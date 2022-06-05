__all__ = ['MessageHandler']

from typing import Callable

from core.settings import Settings


class MessageHandler:
    def __init__(self, settings: Settings):
        self.__observers: dict[str, list[Callable]] = dict()
        self.settings: Settings = settings

    def register(self, title: str, handler: Callable) -> None:
        handlers = self.__observers.setdefault(title, [])
        handlers.append(handler)

    def handle(self, title: str, message: str) -> None:
        handlers = self.__observers.get(title, [])
        for handler in handlers:
            handler(message=message, settings=self.settings)
