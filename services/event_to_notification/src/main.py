import logging
from logging import config as logging_config

from core.logger import LOGGING
from core.settings import get_settings
from services.auth_api.auth_service import AuthAPI
from services.consumers.base import AbstractConsumer
from services.consumers.kafka_consumer import ConsumerKafka
from services.message_handler import MessageHandler
from services.notification_api.notification_service import NotificationAPI
from services.notification_handlers import (
    send_bill_notification_to_user,
    send_refund_notification_to_admin,
    send_refund_notification_to_user,
)

logging_config.dictConfig(LOGGING)
logger = logging.getLogger('event_to_notification')


def start_consume(consumer: AbstractConsumer, message_handler: MessageHandler):
    """Запуск обработки событий."""
    messages = consumer.consume()
    for message in messages:
        message_handler.handle(title=message.key, message=message.value)


def register_observers(mh: MessageHandler):
    """Регистрация слушателей событий по заголовкам (ключам) полученных сообщений."""
    mh.register('bill.refunded', send_refund_notification_to_user)
    mh.register('bill.refunded', send_refund_notification_to_admin)
    mh.register('bill.paid', send_bill_notification_to_user)


if __name__ == '__main__':
    settings = get_settings()
    notification_api = NotificationAPI(api_url=settings.notification_api.url)
    user_auth_service = AuthAPI(
        api_url=settings.auth_api.url,
        username=settings.auth_api.login,
        password=settings.auth_api.password,
    )

    mh = MessageHandler(
        settings=settings,
        notification_service=notification_api,
        user_auth_service=user_auth_service,
    )
    register_observers(mh)

    kafka_consumer = ConsumerKafka(
        bootstrap_servers=settings.kafka.bootstrap_servers,
        auto_offset_reset=settings.kafka.auto_offset_reset,
        enable_auto_commit=settings.kafka.enable_auto_commit,
        group_id=settings.kafka.group_id,
        topics=settings.kafka.topics,
    )

    start_consume(kafka_consumer, mh)
