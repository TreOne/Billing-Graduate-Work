from abc import abstractmethod, ABC

from core.settings import settings
from services.kafka_consumer import ConsumerKafka


class AbstractConsumer(ABC):
    @abstractmethod
    def consume(self):
        ...


class Consumer(AbstractConsumer, ConsumerKafka):
    configs = settings.kafka


