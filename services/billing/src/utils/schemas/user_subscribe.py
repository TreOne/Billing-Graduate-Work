from utils.schemas import FastJsonModel

__all__ = ('UserSubscribeSchema',)


class UserSubscribeSchema(FastJsonModel):
    """Represents incoming user subscribe model."""

    role_uuid: str
    user_uuid: str
