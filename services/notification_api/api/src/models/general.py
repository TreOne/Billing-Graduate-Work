from datetime import datetime, timedelta
from typing import Optional

import orjson
from pydantic import BaseModel, Field


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class FastJsonModel(BaseModel):
    """Модель с быстрым json-сериализатором."""

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class IncomingNotificationSchema(FastJsonModel):
    """Модель сообщения приходящего на ручку."""

    recipient: str
    subject: str
    body: str
    immediately: Optional[bool] = False
    log_it: Optional[bool] = False
    ttl: Optional[int] = 60 * 60 * 24


class StorageMessageSchema(FastJsonModel):
    """Модель сообщения которое храним в брокере."""

    to: str
    subject: str
    body: str
    exp: datetime
    log_it: Optional[bool] = False

    class Config(FastJsonModel.Config):
        json_encoders = {
            datetime: lambda v: v.isoformat(),
        }

    @classmethod
    def from_notification(
        cls, notification: IncomingNotificationSchema
    ) -> 'StorageMessageSchema':
        exp_date = datetime.now() + timedelta(seconds=notification.ttl)
        instance = cls(
            to=notification.recipient,
            subject=notification.subject,
            body=notification.body,
            exp=exp_date,
            log_it=notification.log_it,
        )
        return instance


class Response(FastJsonModel):
    """Ответ от сервера."""

    msg: Optional[str] = Field(title='Сообщение от сервера.', example='OK')
