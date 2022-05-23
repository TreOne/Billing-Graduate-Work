from pydantic import EmailStr

from models.general import IncomingNotificationSchema, StorageMessageSchema


class EmailNotificationSchema(IncomingNotificationSchema):
    """Модель сообщения приходящего на ручку."""

    recipient: EmailStr


class EmailMessageSchema(StorageMessageSchema):
    """Модель сообщения которое храним в брокере."""

    to: EmailStr
