import json
import logging

from celery import shared_task
from django.conf import settings

from billing.models.enums import BillType
from billing.repositories.bill import BillRepository
from utils.auth_api.auth_service import AuthAPI
from utils.schemas.bill import BillBaseSchema

log = logging.getLogger(__name__)


@shared_task
def say_hello():
    logging.info("hello")
    return "success"


@shared_task
def autopay_periodic_task():
    """Задача для автопродление подписки."""
    # Авторизуемся в сервисе Авторизации
    auth_service = AuthAPI(
        username=settings.AUTH_SERVICE_USERNAME,
        password=settings.AUTH_SERVICE_PASSWORD,
    )
    # Получаем оканчивающиеся подписки пользователей, за три дня до окончания
    subscriptions_end: list = auth_service.get_user_subscriptions_end(days=3)
    end_result = []
    for subscription in subscriptions_end:
        # Готовим схему Оплаты
        bill_schema = BillBaseSchema(
            user_uuid=subscription.user_uuid,
            type=BillType.subscription,
            item_uuid=subscription.role_uuid,
        )
        # Покупаем объект подписки для конкретного пользователя
        result: dict = BillRepository.buy_item(bill_schema=bill_schema)
        log.info(result)
        end_result.append(result)
    return json.dumps(end_result)
