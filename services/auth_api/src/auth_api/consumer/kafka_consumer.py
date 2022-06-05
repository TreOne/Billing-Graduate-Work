import json

from kafka import KafkaConsumer


class KafkaConnector:
    """Коннектор к кафке."""

    def __init__(self, kafka_url: str, topic: str):
        self.kafka_url = kafka_url
        self.topic = topic

    def init_consumer(self):
        consumer = KafkaConsumer(
            self.topic,
            bootstrap_servers=self.kafka_url,
            value_deserializer=lambda m: json.loads(m.decode("utf-8")),
        )

        return consumer
