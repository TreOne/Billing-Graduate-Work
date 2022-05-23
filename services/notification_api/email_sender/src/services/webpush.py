from services.general import GeneralSendingService, GeneralService


class WebpushService(GeneralService):
    def __init__(self, sending_service: GeneralSendingService):
        super().__init__(sending_service)

    name = 'webpush'
