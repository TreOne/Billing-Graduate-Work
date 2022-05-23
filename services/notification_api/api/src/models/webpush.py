from models.general import IncomingNotificationSchema, StorageMessageSchema


class WebPushNotificationSchema(IncomingNotificationSchema):
    """Модель сообщения приходящего на ручку."""

    ...


class WebPushMessageSchema(StorageMessageSchema):
    """Модель сообщения которое храним в брокере."""

    ...
