import logging

from core.settings import get_settings
from services.auth_api.auth_service import AuthAPI
from services.consumers.base import AbstractConsumer
from services.consumers.kafka_consumer import ConsumerKafka
from services.message_handler import MessageHandler
from services.notification_api.notification_service import NotificationAPI
from services.notification_handlers import send_bill_notification_to_user, send_refund_notification_to_user, \
    send_refund_notification_to_admin

logger = logging.getLogger(__name__)


def start_consume(consumer: AbstractConsumer, message_handler: MessageHandler):
    messages = consumer.consume()
    for message in messages:
        message_handler.handle(title=message.key, message=message.value)


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
    mh.register('bill.refunded', send_refund_notification_to_user)
    mh.register('bill.refunded', send_refund_notification_to_admin)
    mh.register('bill.paid', send_bill_notification_to_user)

    kafka_consumer = ConsumerKafka(
        bootstrap_servers=settings.kafka.bootstrap_servers,
        auto_offset_reset=settings.kafka.auto_offset_reset,
        enable_auto_commit=settings.kafka.enable_auto_commit,
        group_id=settings.kafka.group_id,
        topics=settings.kafka.topics,
    )

    start_consume(kafka_consumer, mh)
