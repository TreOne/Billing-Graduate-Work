import logging

import orjson

from core.settings import Settings
from services.auth_api.base import AbstractAuth
from services.consumers.models import BillMessage
from services.notification_api.base import AbstractNotificationService, Notification
from services.template_utils.render import render_template

logger = logging.getLogger('event_to_notification')


def send_bill_notification_to_user(
    message: str,
    user_auth_service: AbstractAuth,
    notification_service: AbstractNotificationService,
    settings: Settings,
) -> None:
    bill_message = BillMessage(**orjson.loads(message))
    user_data = user_auth_service.get_user_info(user_uuid=bill_message.user_uuid)
    if not user_data:
        logger.error(f'User not found {bill_message.user_uuid}.')
        return
    template_schema = {
        'username': user_data.username,
        'amount': bill_message.amount,
        'link': settings.project.redirect_url,
    }
    notification_body = render_template(
        template_name='payment_template_bill', data=template_schema,
    )
    notification = Notification(
        recipient=user_data.email,
        subject='Bill_Paid',
        body=notification_body,
        immediately=True,
        log_it=True,
    )
    notification_service.send(notification)


def send_refund_notification_to_user(
    message: str,
    user_auth_service: AbstractAuth,
    notification_service: AbstractNotificationService,
    settings: Settings,
) -> None:
    bill_message = BillMessage(**orjson.loads(message))
    user_data = user_auth_service.get_user_info(user_uuid=bill_message.user_uuid)
    if not user_data:
        logger.error(f'User not found {bill_message.user_uuid}.')
        return
    template_schema = {
        'username': user_data.username,
        'amount': bill_message.amount,
        'link': settings.project.redirect_url,
    }
    notification_body = render_template(
        template_name='refund_template_bill', data=template_schema,
    )
    notification = Notification(
        recipient=user_data.email,
        subject='Bill_refund',
        body=notification_body,
        immediately=True,
        log_it=True,
    )
    notification_service.send(notification)


def send_refund_notification_to_admin(
    message: str,
    user_auth_service: AbstractAuth,
    notification_service: AbstractNotificationService,
    settings: Settings,
) -> None:
    bill_message = BillMessage(**orjson.loads(message))
    template_schema = {
        'username': 'Admin',
        'user_id': bill_message.user_uuid,
        'amount': bill_message.amount,
        'link': settings.project.redirect_url,
    }
    notification_body = render_template(
        template_name='refund_template_admin', data=template_schema,
    )
    notification = Notification(
        recipient=settings.project.admin_email,
        subject='Bill_refund',
        body=notification_body,
        immediately=True,
        log_it=True,
    )
    notification_service.send(notification)
