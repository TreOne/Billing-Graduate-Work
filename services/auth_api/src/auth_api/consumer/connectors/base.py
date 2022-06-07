from abc import ABC, abstractmethod
from typing import Iterator

from auth_api.consumer.models import BillMessage


class AbstractBrokerConnector(ABC):
    """Интерфейс подключения к брокеру сообщений."""

    @abstractmethod
    def get_consumer(self) -> Iterator[BillMessage]:
        raise NotImplementedError
