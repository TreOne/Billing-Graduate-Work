from services.general import GeneralSendingService, GeneralService


class WebsocketService(GeneralService):
    def __init__(self, sending_service: GeneralSendingService):
        super().__init__(sending_service)

    name = 'websocket'
