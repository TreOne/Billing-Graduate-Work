import logging
from typing import Iterator

from kafka import KafkaConsumer

from auth_api.consumer.connectors.base import AbstractBrokerConnector
from auth_api.consumer.models import BillMessage

logger = logging.getLogger('auth_consumer')


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
                logger.error(e,  exc_info=True, extra={'Error processing messages': message.value.dict})
                continue
