from models.base import FastJsonModel


class IncomingNotificationSchema(FastJsonModel):
    """ Represents message to send model ."""
    recipient: str
    subject: str
    body: str
    immediately: bool = False
    log_it: bool = False
    ttl: int = 60 * 60 * 24
