from abc import ABC
from typing import Iterator

from services.consumers.base import AbstractConsumer, BrokerMessage


class ConsumerDummy(AbstractConsumer, ABC):
    def __init__(self, messages: list[BrokerMessage]):
        self.messages = messages

    def consume(self) -> Iterator[BrokerMessage]:
        for message in self.messages:
            yield message
