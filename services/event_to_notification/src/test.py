import logging

from logging import config as logging_config
from core.logger import LOGGING
from core.settings import get_settings
from services.auth_api.auth_service_dummy import DummyAuthAPI
from services.auth_api.base import UserSchema
from services.consumers.base import AbstractConsumer, BrokerMessage
from services.consumers.consumer_dummy import ConsumerDummy
from services.message_handler import MessageHandler
from services.notification_api.notification_service_dummy import DummyNotificationAPI
from services.notification_handlers import (
    send_bill_notification_to_user,
    send_refund_notification_to_user,
    send_refund_notification_to_admin,
)
logging_config.dictConfig(LOGGING)
logger = logging.getLogger('event_to_notification')


def start_consume(consumer: AbstractConsumer, message_handler: MessageHandler):
    messages = consumer.consume()
    for message in messages:
        message_handler.handle(title=message.key, message=message.value)

    for notification in message_handler.notification_service.notifications:
        print(notification)


if __name__ == '__main__':
    settings = get_settings()
    notification_api = DummyNotificationAPI()

    user_auth_service = DummyAuthAPI(
        {
            'a19236ca-2c39-4353-bd82-8b1ea3e59610': UserSchema(
                email='user@example.com', username='ExampleUser'
            ),
            'a19236ca-2c39-4353-bd82-8b1ea3e59611': UserSchema(
                email='user2@example.com', username='ExampleUser2'
            ),
        }
    )

    mh = MessageHandler(
        settings=settings,
        notification_service=notification_api,
        user_auth_service=user_auth_service,
    )
    mh.register('bill.refunded', send_refund_notification_to_user)
    mh.register('bill.refunded', send_refund_notification_to_admin)
    mh.register('bill.paid', send_bill_notification_to_user)

    dummy_consumer = ConsumerDummy(
        [
            BrokerMessage(
                key='bill.refunded',
                value="""
                {
                    "bill_uuid": "84b27fc2-775e-40c9-9d81-41ec1b1ec85a",
                    "status": "created",
                    "user_uuid": "a19236ca-2c39-4353-bd82-8b1ea3e59610",
                    "type": "subscription",
                    "item_uuid": "0e29f833-164f-47ce-8002-392e1c3114cc",
                    "amount": 300.0
                }
            """,
            ),
            BrokerMessage(
                key='bill.refunded',
                value="""
                {
                    "bill_uuid": "3fbf05e8-5d03-4040-bc68-3224ca318363",
                    "status": "created",
                    "user_uuid": "a19236ca-2c39-4353-bd82-8b1ea3e59610",
                    "type": "movie",
                    "item_uuid": "f49bd3ee-ab7e-4309-9334-c2ac1686ba99",
                    "amount": 150.0
                }
            """,
            ),
            BrokerMessage(
                key='bill.paid',
                value="""
                {
                    "bill_uuid": "84b27fc2-775e-40c9-9d81-41ec1b1ec85a",
                    "status": "paid",
                    "user_uuid": "a19236ca-2c39-4353-bd82-8b1ea3e59610",
                    "type": "subscription",
                    "item_uuid": "0e29f833-164f-47ce-8002-392e1c3114cc",
                    "amount": 300.0
                }
            """,
            ),
        ]
    )

    start_consume(dummy_consumer, mh)
