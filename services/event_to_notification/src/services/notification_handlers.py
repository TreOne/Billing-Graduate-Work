import logging

import orjson

from services.auth_api.base import AbstractAuth
from services.consumers.models import BillMessage
from services.notification_api.base import AbstractNotificationService, Notification
from services.template_utils.render import render_template, TemplateBodySchema

logger = logging.getLogger(__name__)


def send_bill_notification_to_user(
        message: str,
        user_auth_service: AbstractAuth,
        notification_service: AbstractNotificationService
) -> None:
    bill_message = BillMessage(**orjson.loads(message))
    user_data = user_auth_service.get_user_info(user_uuid=bill_message.user_uuid)
    if not user_data:
        logger.error(f'User not found {bill_message.user_uuid}.')
        return
    template_schema = TemplateBodySchema(
        username=user_data.username,
        amount=bill_message.amount
    )
    notification_body = render_template(
        template_name='payment_bill',
        data=template_schema.dict(),
    )
    notification = Notification(
        recipient=user_data.email,
        subject='Счёт',
        body=notification_body,
        immediately=True,
    )
    notification_service.send(notification)


def send_paid_notification_to_user(
        message: dict[str, any],
        user_auth_service: AbstractAuth,
        notification_service: AbstractNotificationService,
) -> None:
    logger.error(message)
