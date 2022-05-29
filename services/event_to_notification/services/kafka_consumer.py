__all__ = ["ConsumerKafka"]

import logging
from abc import abstractmethod, ABC

import backoff
from kafka import KafkaConsumer

from core.settings import settings, KafkaTaskSettings

logger = logging.getLogger(__name__)


class ConsumerKafka(ABC):
    def __init__(self):
        self.conn = None

    @property
    @abstractmethod
    def configs(self) -> KafkaTaskSettings:
        pass

    @backoff.on_exception(
        wait_gen=backoff.expo,
        exception=(RuntimeError, ConnectionError, TimeoutError),
        max_time=settings.backoff_timeout,
    )
    def get_consumer(self) -> None:
        if not self.conn:
            self.conn: KafkaConsumer = KafkaConsumer(
                security_protocol="PLAINTEXT",
                bootstrap_servers=self.configs.bootstrap_servers,
                auto_offset_reset="earliest",
                enable_auto_commit=False,
                group_id="$Default",
                value_deserializer=lambda x: x.decode("utf-8"),
                reconnect_backoff_ms=100,
            )
