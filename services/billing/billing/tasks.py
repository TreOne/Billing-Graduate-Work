import logging

from celery import shared_task

log = logging.getLogger(__name__)


@shared_task
def friday_top_email():
    """Задача для отправки топа фильмов недели по почте."""
    pass
