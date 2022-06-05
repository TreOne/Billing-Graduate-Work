import logging
from datetime import datetime
from celery import shared_task
from billing.repositories import UserAutoPayRepository

log = logging.getLogger(__name__)


@shared_task
def autopay_periodic_task():
    """Задача для автопродление подписки."""
    auto_pays = UserAutoPayRepository
    print(f"hello {datetime.now()}")
