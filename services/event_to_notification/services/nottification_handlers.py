import logging


def send_created_notification_to_user(message: str):
    logger = logging.getLogger(__name__)
    logger.error(message)


def send_paid_notification_to_user(message: str):
    logger = logging.getLogger(__name__)
    logger.error(message)

