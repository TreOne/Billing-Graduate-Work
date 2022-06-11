import logging

from fastapi import APIRouter, Depends

from models.email import EmailNotificationSchema
from models.general import Response
from services.email import EmailService
from services.getters import get_email_service, get_webpush_service, get_websocket_service
from services.webpush import WebpushService
from services.websocket import WebsocketService

router = APIRouter(prefix='/send')
logger = logging.getLogger('notification_api')


@router.post(
    path='/email', name='Отправка письма.', response_model=Response,
)
async def email_registration(
    email: EmailNotificationSchema, email_service: EmailService = Depends(get_email_service)
) -> Response:
    response = await email_service.register(email)
    return response


@router.post(
    path='/websocket', name='Отправка websocket уведомления.', response_model=Response,
)
async def websocket_registration(
    websocket_notification: EmailNotificationSchema,
    websocket_service: WebsocketService = Depends(get_websocket_service),
) -> Response:
    response = await websocket_service.register(websocket_notification)
    return response


@router.post(
    path='/web-push', name='Отправка web-push уведомления.', response_model=Response,
)
async def webpush_registration(
    webpush_notification: EmailNotificationSchema,
    webpush_service: WebpushService = Depends(get_webpush_service),
) -> Response:
    response = await webpush_service.register(webpush_notification)
    return response
