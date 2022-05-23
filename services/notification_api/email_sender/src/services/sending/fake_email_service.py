from core.models import StorageMessageSchema

from services.general import GeneralSendingService


class ConsoleEmailSendingService(GeneralSendingService):
    """Фэйковый сервис отправки сообщений в консоль."""

    def send(self, message: StorageMessageSchema):
        print(message)
