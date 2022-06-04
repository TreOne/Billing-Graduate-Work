__all__ = ["ConsumerKafka"]

import logging
from typing import Optional, NamedTuple

import backoff
from kafka import KafkaConsumer

from core.settings import get_settings, KafkaTaskSettings
from services.base_services import AbstractConsumer

logger = logging.getLogger(__name__)
settings = get_settings()


class ConsumerKafka(AbstractConsumer):
    def __init__(self, configs: KafkaTaskSettings):
        self.consumer: Optional[KafkaConsumer] = None
        self.configs = configs

    @backoff.on_exception(
        wait_gen=backoff.expo,
        exception=(RuntimeError, ConnectionError, TimeoutError),
        max_time=settings.backoff_timeout,
    )
    def start_consumer(self) -> None:
        if not self.consumer:
            self.consumer: KafkaConsumer = KafkaConsumer(
                security_protocol="PLAINTEXT",
                bootstrap_servers=self.configs.bootstrap_servers,
                auto_offset_reset=self.configs.auto_offset_reset,
                enable_auto_commit=self.configs.enable_auto_commit,
                key_deserializer=None,
                group_id=self.configs.group_id,
                reconnect_backoff_ms=100,
            )
            self.consumer.subscribe(topics=self.configs.topics)

    def stop_consumer(self) -> None:
        self.consumer.close()

    def consume(self) -> NamedTuple:
        self.start_consumer()
        while True:
            for message in self.consumer:
                yield message
            self.consumer.commit()
