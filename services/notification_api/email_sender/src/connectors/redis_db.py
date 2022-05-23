import logging
from typing import Optional

import backoff
from redis import Redis

from core.utils import backoff_hdlr
from settings.settings import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()
redis_connection: Optional[Redis] = None


def get_redis() -> Redis:
    """Возвращает объект для асинхронного общения с сервисами Redis.
    Функция понадобится при внедрении зависимостей."""
    return redis_connection


@backoff.on_exception(backoff.expo, ConnectionError, on_backoff=backoff_hdlr)
def redis_ping():
    """Проверяет подключение к сервису Redis."""
    global redis_connection
    ping = redis_connection.ping()
    if not ping:
        raise ConnectionError('The redis server is not responding.')


def redis_connect():
    """Устанавливает подключение к сервису Redis."""
    global redis_connection
    redis_connection = Redis(host=settings.redis.host, port=settings.redis.port, db=1,)
    redis_ping()
    logger.info('Successfully connected to redis server.')


def redis_disconnect():
    """Закрывает подключение к сервису Redis."""
    global redis_connection
    redis_connection.close()
    logger.info('Successfully disconnected from redis server.')
