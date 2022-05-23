import logging
from abc import ABCMeta, abstractmethod
from datetime import date, datetime

from core.models import StorageMessageSchema

from connectors.rabbitmq import get_rmq_channel
from connectors.redis_db import get_redis
from settings.settings import get_settings

logger = logging.getLogger('email_sender')
settings = get_settings()


class GeneralSendingService(metaclass=ABCMeta):
    """Интерфейс сервиса отправки сообщений."""

    @abstractmethod
    def send(self, message: StorageMessageSchema):
        raise NotImplementedError


class GeneralService(metaclass=ABCMeta):
    def __init__(self, sending_service: GeneralSendingService):
        self._rmq_channel = get_rmq_channel()
        self._redis = get_redis()
        self._sending_service = sending_service

    @property
    @abstractmethod
    def name(self):
        """Название сервиса. Используется для создания ключей кэша, очередей в брокере сообщений и т.д."""
        pass

    def general_callback(self, ch, method, properties, body):
        """Колбек функция для использования в basic_consume."""
        message: StorageMessageSchema = StorageMessageSchema.from_message(body)
        try:
            self._send_general(message)
        except Exception as e:
            self._send_message_to_trouble_queue(message, reason=str(e))
            logger.error(e, exc_info=True, extra={'Message': body})
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def urgent_callback(self, ch, method, properties, body):
        """Колбек функция для использования в basic_consume."""
        message: StorageMessageSchema = StorageMessageSchema.from_message(body)
        try:
            self._send_urgent(message)
        except Exception as e:
            self._send_message_to_trouble_queue(message, reason=str(e))
            logger.error(e, exc_info=True, extra={'Message': body})
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def _send_general(self, message: StorageMessageSchema) -> bool:
        """Отправляет обычное сообщение."""
        general_limit = settings.email.daily_limit - settings.email.urgent_reserve
        if self._get_daily_count() >= general_limit:
            self._send_message_to_trouble_queue(
                message, reason='The limit of general messages has been reached.'
            )
            return False

        if datetime.now() > message.exp:
            self._send_message_to_trouble_queue(
                message, reason='The message has expired and is no longer relevant.'
            )
            return False

        if message.log_it:
            logger.info('Sending general message.', extra=message.dict())

        self._sending_service.send(message)
        self._incr_daily_count()
        return True

    def _send_urgent(self, message: StorageMessageSchema) -> bool:
        """Отправляет моментальное сообщение."""
        if self._get_daily_count() >= settings.email.daily_limit:
            self._send_message_to_trouble_queue(
                message, reason='The limit of urgent messages has been reached.'
            )
            return False

        if datetime.now() > message.exp:
            self._send_message_to_trouble_queue(
                message, reason='The message has expired and is no longer relevant.'
            )
            return False

        if message.log_it:
            logger.info('Sending urgent message.', extra=message.dict())

        self._sending_service.send(message)
        self._incr_daily_count()
        return True

    def _get_daily_count(self) -> int:
        """Возвращает количество сообщений за день."""
        notification_count = self._redis.get(f'count_{self.name}::{date.today()}')
        notification_count = int(notification_count) if notification_count else 0
        return notification_count

    def _incr_daily_count(self) -> None:
        """Увеличивает количество сообщений за день."""
        self._redis.incr(f'count_{self.name}::{date.today()}')

    def _send_message_to_trouble_queue(self, message: StorageMessageSchema, reason=None):
        """Отправляет сообщение в очередь проблемных."""
        body = message.json().encode('utf-8')
        self._rmq_channel.basic_publish(
            exchange='general_exchange', routing_key=f'{self.name}.trouble', body=body,
        )
        logger.error(reason if reason else 'Unknown reason', extra={'Message': body})
