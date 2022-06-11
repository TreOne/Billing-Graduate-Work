import hashlib
import logging
from abc import ABCMeta, abstractmethod
from http import HTTPStatus

from fastapi import HTTPException

from connectors.rabbitmq import get_rmq_channel
from connectors.redis import get_redis
from models.general import IncomingNotificationSchema, Response, StorageMessageSchema

logger = logging.getLogger('notification_api')


class GeneralService(metaclass=ABCMeta):
    def __init__(self):
        self._rmq_channel = get_rmq_channel()
        self._redis = get_redis()

    @property
    @abstractmethod
    def name(self):
        """Название сервиса. Используется для создания ключей кэша, очередей в брокере сообщений и т.д."""
        pass

    async def register(self, notification: IncomingNotificationSchema) -> Response:
        """Регистрирует получение уведомления в очереди RabbitMQ."""
        cache_key = self._get_notification_cache_key(notification)
        if await self._redis.get(key=cache_key) is not None:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Re-sending the same message is prohibited.',
            )

        if notification.log_it:
            logger.info('A notification request was received.', extra=notification.dict())

        routing_key = self._get_routing_key(notification)
        message = StorageMessageSchema.from_notification(notification)
        self._publish_message(routing_key, message)

        await self._redis.set(key=cache_key, value='', expire=notification.ttl)
        return Response(msg='ОК')

    def _get_notification_cache_key(self, notification: IncomingNotificationSchema) -> str:
        """Возвращает ключ по которому можно отследить уникальность уведомления."""
        body_hash = hashlib.md5(notification.body.encode('utf-8')).hexdigest()
        return f'{self.name}::{notification.recipient}::{notification.subject}::{body_hash}'

    def _get_routing_key(self, notification: IncomingNotificationSchema) -> str:
        """Возвращает ключ от очереди с уведомлениями."""
        if notification.immediately:
            return f'{self.name}.urgent'

        return f'{self.name}.general'

    def _publish_message(self, routing_key: str, message: StorageMessageSchema):
        """Публикует сообщение в RabbitMQ."""
        self._rmq_channel.basic_publish(
            exchange='general_exchange',
            routing_key=routing_key,
            body=message.json().encode('utf-8'),
        )
