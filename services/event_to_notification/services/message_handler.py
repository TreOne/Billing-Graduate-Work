from typing import Callable, Dict, List


class MessageHandler:
    def __init__(self):
        self.__observers: Dict[str, List[Callable]] = dict()

    def register(self, title: str, handler: Callable):
        handlers = self.__observers.setdefault(title, [])
        handlers.append(handler)

    def handle(self, title: str, message: str):
        handlers = self.__observers.get(title, [])
        for handler in handlers:
            handler(message)
