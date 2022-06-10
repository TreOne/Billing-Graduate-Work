import logging
from abc import ABC
from typing import Optional, Iterator

import backoff
from kafka import KafkaConsumer

from services.consumers.base import AbstractConsumer, BrokerMessage

logger = logging.getLogger(__name__)


class ConsumerKafka(AbstractConsumer, ABC):
    def __init__(
            self,
            bootstrap_servers: str,
            auto_offset_reset: str,
            enable_auto_commit: str,
            group_id: str,
            topics: Optional[list[str]],
    ):
        self.bootstrap_servers = bootstrap_servers
        self.auto_offset_reset = auto_offset_reset
        self.enable_auto_commit = enable_auto_commit
        self.group_id = group_id
        self.topics = topics
        self.consumer: Optional[KafkaConsumer] = None

    def consume(self) -> Iterator[BrokerMessage]:
        self.start_consumer()
        try:
            while True:
                for message in self.consumer:
                    yield BrokerMessage(key=message.key.decode('UTF-8'), value=message.value.decode('UTF-8'))
                self.consumer.commit()
        finally:
            self.stop_consumer()

    @backoff.on_exception(
        wait_gen=backoff.expo,
        exception=(RuntimeError, ConnectionError, TimeoutError),
        max_tries=4,
    )
    def start_consumer(self) -> None:
        if not self.consumer:
            self.consumer: KafkaConsumer = KafkaConsumer(
                security_protocol='PLAINTEXT',
                bootstrap_servers=self.bootstrap_servers,
                auto_offset_reset=self.auto_offset_reset,
                enable_auto_commit=self.enable_auto_commit,
                group_id=self.group_id,
                reconnect_backoff_ms=100,
            )
            self.consumer.subscribe(topics=self.topics)
            logger.info('Successfully connected to kafka server.')

    def stop_consumer(self) -> None:
        self.consumer.close()
