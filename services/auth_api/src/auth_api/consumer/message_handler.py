from typing import Callable, Dict, List

from models import Message

class MessageHandler:
    def __init__(self):
        self.__observers: Dict[str, List[Callable]] = dict()

    def register(self, title: str, handler: Callable):
        handlers = self.__observers.setdefault(title, [])
        handlers.append(handler)

    def handle(self, message: Message):
        handlers = self.__observers.get(message.title, [])
        for handler in handlers:
            handler(message.body)