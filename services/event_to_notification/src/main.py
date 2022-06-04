import logging

from core.settings import get_settings, settings_res
from services.kafka_consumer import ConsumerKafka
from services.message_handler import MessageHandler

message_handler = None
logger = logging.getLogger(__name__)

settings = settings_res


def main():
    consumer = ConsumerKafka(settings.kafka)
    messages = consumer.consume()
    for message in messages:
        message_handler.handle(title=message.key.decode('UTF-8'), message=message.value)


if __name__ == '__main__':
    message_handler = MessageHandler()
    for task in settings.tasks:
        message_handler.register(task.title, task.handler)
    main()
