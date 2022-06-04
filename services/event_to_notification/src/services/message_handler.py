__all__ = ["MessageHandler"]

from typing import Callable


class MessageHandler:
    def __init__(self):
        self.__observers: dict[str, list[Callable]] = dict()

    def register(self, title: str, handler: Callable) -> None:
        handlers = self.__observers.setdefault(title, [])
        handlers.append(handler)

    def handle(self, title: str, message: str) -> None:
        handlers = self.__observers.get(title, [])
        for handler in handlers:
            handler(message)
