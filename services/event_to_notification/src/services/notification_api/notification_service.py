import logging
from http import HTTPStatus

import requests

from services.notification_api.base import AbstractNotificationService, Notification

logger = logging.getLogger('event_to_notification')


class NotificationAPI(AbstractNotificationService):
    """Реализация интерфейса отправки уведомлений."""

    def __init__(self, api_url: str):
        self.api_url = api_url

    def send(self, notification: Notification) -> bool:
        response = requests.post(self.api_url, data=notification.json())
        if response.status_code != HTTPStatus.OK:
            logging.error(f" Not able to  send notification to  user {notification.recipient}")
        return response.status_code == HTTPStatus.OK
