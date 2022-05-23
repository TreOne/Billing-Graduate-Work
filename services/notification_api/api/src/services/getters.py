from functools import lru_cache

from services.email import EmailService
from services.webpush import WebpushService
from services.websocket import WebsocketService


@lru_cache
def get_email_service() -> EmailService:
    return EmailService()


@lru_cache
def get_websocket_service() -> WebsocketService:
    return WebsocketService()


@lru_cache
def get_webpush_service() -> WebpushService:
    return WebpushService()
