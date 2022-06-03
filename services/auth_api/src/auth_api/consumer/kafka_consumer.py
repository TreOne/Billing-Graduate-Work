import json

from kafka import KafkaConsumer, KafkaProducer
from kafka.structs import TopicPartition

from auth_api.consumer import message_handler
from auth_api.consumer.models import Message


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

    # def consume_kafka(self, message_handler):
    #     consumer = self.init_consumer()
    #     try:
    #         for message in consumer:
    #             title = message.key.decode("utf-8")
    #             body = message.value
    #             message = Message(title=title, body=body)
    #             message_handler.handle(message)
    #
    #     except Exception as exe:
    #         print(f"Возникла ошибка при получении сообщений из кафки:{exe}")


