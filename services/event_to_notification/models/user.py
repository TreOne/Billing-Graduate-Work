from models.base import FastJsonModel


class UserSchema(FastJsonModel):
    email: str
    username: str
