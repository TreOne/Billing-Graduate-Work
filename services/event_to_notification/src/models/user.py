from models.base import FastJsonModel


class UserSchema(FastJsonModel):
    """Represents incoming user  model ."""

    email: str
    username: str
