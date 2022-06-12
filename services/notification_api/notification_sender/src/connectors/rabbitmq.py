import logging
from typing import Optional

import backoff
from pika import ConnectionParameters, credentials
from pika.adapters.blocking_connection import BlockingChannel, BlockingConnection

from core.utils import backoff_hdlr
from settings.settings import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()
rmq_channel: Optional[BlockingChannel] = None
rmq_connection: Optional[BlockingConnection] = None


def get_rmq_channel() -> BlockingChannel:
    """Возвращает объект для общения с сервисами RabbitMQ.
    Функция понадобится при внедрении зависимостей."""
    return rmq_channel


@backoff.on_exception(backoff.expo, RuntimeError, on_backoff=backoff_hdlr)
def rabbitmq_connect():
    """Устанавливает подключение к RabbitMQ."""
    global rmq_channel
    global rmq_connection
    rmq_parameters = ConnectionParameters(
        host=settings.rabbitmq.host,
        port=settings.rabbitmq.port,
        credentials=credentials.PlainCredentials(
            username=settings.rabbitmq.user, password=settings.rabbitmq.password,
        ),
    )
    logger.info('Establishing a connection to RabbitMQ.')
    rmq_connection = BlockingConnection(rmq_parameters)
    rmq_channel = rmq_connection.channel()
    logger.info('A connection to RabbitMQ has been established.')


def rabbitmq_prepare():
    """Конфигурация RabbitMQ."""
    global rmq_channel

    rmq_channel.exchange_declare(
        exchange='general_exchange',
        exchange_type='direct',
        passive=False,
        durable=True,
        auto_delete=False,
    )

    rmq_channel.queue_declare(queue='email.urgent', durable=True)
    rmq_channel.queue_declare(queue='email.general', durable=True)
    rmq_channel.queue_declare(queue='email.trouble', durable=True)
    rmq_channel.queue_bind(
        queue='email.urgent', exchange='general_exchange', routing_key='email.urgent'
    )
    rmq_channel.queue_bind(
        queue='email.general', exchange='general_exchange', routing_key='email.general'
    )
    rmq_channel.queue_bind(
        queue='email.trouble', exchange='general_exchange', routing_key='email.trouble'
    )

    rmq_channel.queue_declare(queue='websocket.urgent', durable=True)
    rmq_channel.queue_declare(queue='websocket.general', durable=True)
    rmq_channel.queue_declare(queue='websocket.trouble', durable=True)
    rmq_channel.queue_bind(
        queue='websocket.urgent', exchange='general_exchange', routing_key='websocket.urgent'
    )
    rmq_channel.queue_bind(
        queue='websocket.general', exchange='general_exchange', routing_key='websocket.general'
    )
    rmq_channel.queue_bind(
        queue='websocket.trouble', exchange='general_exchange', routing_key='websocket.trouble'
    )

    rmq_channel.queue_declare(queue='webpush.urgent', durable=True)
    rmq_channel.queue_declare(queue='webpush.general', durable=True)
    rmq_channel.queue_declare(queue='webpush.trouble', durable=True)
    rmq_channel.queue_bind(
        queue='webpush.urgent', exchange='general_exchange', routing_key='webpush.urgent'
    )
    rmq_channel.queue_bind(
        queue='webpush.general', exchange='general_exchange', routing_key='webpush.general'
    )
    rmq_channel.queue_bind(
        queue='webpush.trouble', exchange='general_exchange', routing_key='webpush.trouble'
    )

    rmq_channel.basic_qos(prefetch_count=1)


def rabbitmq_disconnect():
    """Закрывает подключение к RabbitMQ."""
    global rmq_connection
    rmq_connection.close()
    logger.info('Successfully disconnected from RabbitMQ.')
