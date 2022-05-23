from datetime import datetime
from typing import Optional

import orjson
from pydantic import BaseModel


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class FastJsonModel(BaseModel):
    """Модель с быстрым json-сериализатором."""

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class StorageMessageSchema(FastJsonModel):
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
    def from_message(cls, message: str) -> 'StorageMessageSchema':
        message = orjson.loads(message)
        message['exp'] = datetime.fromisoformat(message['exp'])
        instance = cls(**message)
        return instance
