from http import HTTPStatus

import requests

from services.notification_api.base import AbstractNotificationService, Notification


class NotificationAPI(AbstractNotificationService):
    """Реализация интерфейса отправки уведомлений."""

    def __init__(self, api_url: str):
        self.api_url = api_url

    def send(self, notification: Notification) -> bool:
        response = requests.post(self.api_url, data=notification.json())
        return response.status_code == HTTPStatus.OK
