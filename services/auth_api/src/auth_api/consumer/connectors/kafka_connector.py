from typing import Iterator

from kafka import KafkaConsumer

from auth_api.consumer.connectors.base import AbstractBrokerConnector
from auth_api.consumer.models import BillMessage


class KafkaConnector(AbstractBrokerConnector):
    """Коннектор к кафке."""

    def __init__(self, host: str, topic: str):
        self.host = host
        self.topic = topic

    def get_consumer(self) -> Iterator[BillMessage]:
        consumer = KafkaConsumer(self.topic, bootstrap_servers=self.host)
        for message in consumer:
            try:
                yield BillMessage.from_message(message)
            except KeyError as e:
                print(f'Ошибка при обработке сообщения "{message.value}": {str(e)}')
                continue
