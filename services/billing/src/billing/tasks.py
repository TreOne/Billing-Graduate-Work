import json
import logging
from logging import config as logging_config

from celery import shared_task
from django.conf import settings

from billing.models.enums import BillType
from billing.repositories.bill import BillRepository
from utils.auth_api.auth_service import AuthAPI
from utils.schemas.bill import BillBaseSchema

# Применяем настройки логирования
logging_config.dictConfig(settings.LOGGING)
logger = logging.getLogger('celery')


@shared_task
def say_hello():
    logger.info('hello')
    return 'success'


@shared_task
def autopay_periodic_task():
    """Задача для автопродление подписки."""
    logger.info('Авторизуемся в сервисе Авторизации')
    auth_service = AuthAPI(
        username=settings.AUTH_SERVICE_USERNAME, password=settings.AUTH_SERVICE_PASSWORD,
    )
    logger.info('Получаем оканчивающиеся подписки пользователей, за три дня до окончания')
    subscriptions_end: list = auth_service.get_user_subscriptions_end(days=3)
    end_result = []
    for subscription in subscriptions_end:
        logger.info('Готовим схему Оплаты')
        bill_schema = BillBaseSchema(
            user_uuid=subscription.user_uuid,
            type=BillType.subscription,
            item_uuid=subscription.role_uuid,
        )
        logger.info(
            f'Покупаем объект подписки ({subscription.role_uuid}) для пользователя {subscription.user_uuid}'
        )
        result: dict = BillRepository.buy_item(bill_schema=bill_schema)
        logger.info('Результат покупки:', extra=result)
        end_result.append(result)
    return json.dumps(end_result)
