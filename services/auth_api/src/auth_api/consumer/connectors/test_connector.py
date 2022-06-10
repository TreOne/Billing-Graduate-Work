import time
from typing import Iterator, List, Optional

from auth_api.consumer.connectors.base import AbstractBrokerConnector
from auth_api.consumer.models import BillMessage


class TestConnector(AbstractBrokerConnector):
    """Коннектор имитирующий подключение к брокеру сообщений."""

    def __init__(self, messages: List[BillMessage], delay: Optional[int] = None):
        self.messages = messages
        self.delay = delay

    def get_consumer(self) -> Iterator[BillMessage]:
        for message in self.messages:
            yield message
            if self.delay:
                time.sleep(self.delay)
