import os
from logging import config as logging_config

from .logger import LOGGING

# Применяем настройки логирования
logging_config.dictConfig(LOGGING)

# Настройки проекта.
PROJECT_NAME: str = 'Сервис отправки уведомлений'

# RabbitMQ
RABBITMQ_USER = os.getenv('RABBITMQ_USER', 'admin')
RABBITMQ_PASS = os.getenv('RABBITMQ_PASS', 'admin')
RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'rabbitmq')
RABBITMQ_PORT = int(os.getenv('RABBITMQ_PORT', 5672))

# Redis
REDIS_HOST = os.getenv('REDIS_HOST', 'redis')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
