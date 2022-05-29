from abc import ABC, abstractmethod

from confluent_kafka import Message


class TransferClass(ABC):

    @staticmethod
    @abstractmethod
    def create_from_message(message: Message) -> 'TransferClass':
        pass
