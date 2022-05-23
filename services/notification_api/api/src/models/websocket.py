from models.general import IncomingNotificationSchema, StorageMessageSchema


class WebsocketNotificationSchema(IncomingNotificationSchema):
    """Модель сообщения приходящего на ручку."""

    ...


class WebsocketMessageSchema(StorageMessageSchema):
    """Модель сообщения которое храним в брокере."""

    ...
