from services.notification_api.base import AbstractNotificationService, Notification


class DummyNotificationAPI(AbstractNotificationService):
    """Реализация интерфейса отправки уведомлений."""

    def __init__(self):
        self.notifications: list[Notification] = []

    def send(self, notification: Notification) -> bool:
        self.notifications.append(notification)
        return True
