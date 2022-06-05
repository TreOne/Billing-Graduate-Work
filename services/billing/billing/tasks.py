import logging

from celery import shared_task

log = logging.getLogger(__name__)


@shared_task
def autopay_periodic_task():
    """Задача для автопродление подписки."""
    pass
