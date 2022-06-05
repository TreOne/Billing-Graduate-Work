from pydantic import BaseModel

from models.base import FastJsonModel


class TemplateBodySchema(BaseModel):
    """ Represents  template data model ."""

    link: str = 'https://pastseason.ru/'
    user: str
    amount: int


class NotificationSchema(FastJsonModel):
    """ Represents message to send model ."""

    recipient: str
    subject: str
    body: str
    immediately: bool = False
    log_it: bool = False
    ttl: int = 60 * 60 * 24
