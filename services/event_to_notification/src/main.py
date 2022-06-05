import logging

from core.settings import get_settings
from services.base_services import Consumer
from services.message_handler import MessageHandler

message_handler = None
logger = logging.getLogger(__name__)

settings = get_settings()


def main():
    consumer = Consumer()
    messages = consumer.consume()
    for message in messages:
        message_handler.handle(title=message.key.decode('UTF-8'), message=message.value)


if __name__ == '__main__':
    message_handler = MessageHandler(settings=settings)
    for task in settings.tasks:
        message_handler.register(task.title, task.handler)
    main()
