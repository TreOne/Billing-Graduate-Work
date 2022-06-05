from confluent_kafka import Producer
from django.conf import settings

producer = Producer(
    {
        "bootstrap.servers": f"{settings.KAFKA_HOST}:{settings.KAFKA_PORT}",
    }
)
