import logging
from logging import config as logging_config

from connectors.rabbitmq import (
    get_rmq_channel,
    rabbitmq_connect,
    rabbitmq_disconnect,
    rabbitmq_prepare,
)
from connectors.redis_db import redis_connect, redis_disconnect
from core.logger import LOGGING
from services.email import EmailService
from services.sending.fake_email_service import ConsoleEmailSendingService
from services.sending.fake_webpush_service import ConsoleWebpushSendingService
from services.sending.fake_websocket_service import ConsoleWebsocketSendingService
from services.webpush import WebpushService
from services.websocket import WebsocketService

logging_config.dictConfig(LOGGING)
logger = logging.getLogger('notification_sender')


if __name__ == '__main__':
    rabbitmq_connect()
    rabbitmq_prepare()
    redis_connect()

    email_to_console = ConsoleEmailSendingService()
    email_service = EmailService(sending_service=email_to_console)

    websocket_to_console = ConsoleWebsocketSendingService()
    websocket_service = WebsocketService(sending_service=websocket_to_console)

    webpush_to_console = ConsoleWebpushSendingService()
    webpush_service = WebpushService(sending_service=webpush_to_console)

    rmq_channel = get_rmq_channel()
    rmq_channel.basic_qos(prefetch_count=1)
    rmq_channel.basic_consume('email.urgent', email_service.urgent_callback)
    rmq_channel.basic_consume('email.general', email_service.general_callback)
    rmq_channel.basic_consume('websocket.urgent', websocket_service.general_callback)
    rmq_channel.basic_consume('websocket.general', websocket_service.urgent_callback)
    rmq_channel.basic_consume('webpush.urgent', webpush_service.general_callback)
    rmq_channel.basic_consume('webpush.general', webpush_service.urgent_callback)
    rmq_channel.start_consuming()
    rabbitmq_disconnect()
    redis_disconnect()
