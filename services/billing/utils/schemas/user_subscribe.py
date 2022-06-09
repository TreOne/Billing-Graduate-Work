from utils.schemas import FastJsonModel


class UserSubscribeSchema(FastJsonModel):
    """Represents incoming user subscribe model."""

    role_uuid: str
    user_uuid: str
