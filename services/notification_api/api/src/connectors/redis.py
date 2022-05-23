import logging
from typing import Optional

import aioredis.errors
import backoff
from aioredis import Redis

from core.config import REDIS_HOST, REDIS_PORT
from core.utils import backoff_hdlr

logger = logging.getLogger(__name__)
redis: Optional[Redis] = None


def get_redis() -> Redis:
    """Возвращает объект для асинхронного общения с сервисами Redis.
    Функция понадобится при внедрении зависимостей."""
    return redis


@backoff.on_exception(backoff.expo, ConnectionError, on_backoff=backoff_hdlr)
async def redis_ping():
    """Проверяет подключение к сервису Redis."""
    global redis
    ping = await redis.ping()
    if ping != b'PONG':
        raise ConnectionError('The redis server is not responding.')


async def redis_connect():
    """Устанавливает подключение к сервису Redis."""
    global redis
    redis = await aioredis.create_redis_pool(
        (REDIS_HOST, REDIS_PORT), db=0, minsize=10, maxsize=20,
    )
    await redis_ping()
    logger.info('Successfully connected to redis server.')


async def redis_disconnect():
    """Закрывает подключение к сервису Redis."""
    global redis
    redis.close()
    await redis.wait_closed()
    logger.info('Successfully disconnected from redis server.')
