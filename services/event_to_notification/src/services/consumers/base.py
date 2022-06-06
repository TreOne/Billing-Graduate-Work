from abc import abstractmethod, ABC
from dataclasses import dataclass
from typing import Iterator


@dataclass(frozen=True)
class BrokerMessage:
    """Тип возвращаемого из потребителя сообщения."""
    key: str
    value: str


class AbstractConsumer(ABC):
    """Интерфейс потребителя сообщений из брокера."""

    @abstractmethod
    def consume(self) -> Iterator[BrokerMessage]:
        """Возвращает итератор по сообщениям."""
        raise NotImplementedError
