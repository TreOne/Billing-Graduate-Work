import logging

from orjson import orjson

from core.settings import settings
from models.bill import IncomingBill
from models.message import TemplateBodySchema, NotificationSchema
from models.user import UserSchema
from services.base_services import get_auth_api
from services.base_utils import render_template, send_message

user_auth_service = get_auth_api()
user_auth_service.login(username=settings.auth_login,
                        password=settings.auth_password)

NOTIFICATION_URL = settings.notification_api_url


def send_bill_notification_to_user(message: dict[str, any]) -> None:
    incoming_message = IncomingBill(**orjson.loads(message))

    user_data_response = user_auth_service.get_user_info(
        user_uuid=incoming_message.user_uuid)

    user_data = UserSchema(**orjson.loads(user_data_response))

    template_schema = TemplateBodySchema(username=user_data.username,
                                         amount=incoming_message.amount)

    rendered_template_body = render_template(data=template_schema.dict(),
                                             template_name='payment_bill')

    result = NotificationSchema(recipient=user_data.email,
                                body=rendered_template_body,
                                immediately=True,
                                subject='bill'
                                )
    send_message(url=NOTIFICATION_URL, message=orjson.dumps(result))


def send_paid_notification_to_user(message: str):
    logger = logging.getLogger(__name__)
    logger.error(message)
