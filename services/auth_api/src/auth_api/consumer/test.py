import logging
from logging import config as logging_config

from auth_api.consumer.connectors.base import AbstractBrokerConnector
from auth_api.consumer.connectors.test_connector import TestConnector
from auth_api.consumer.handlers import add_role_to_user, delete_user_role
from auth_api.consumer.logger import LOGGING
from auth_api.consumer.message_handler import MessageHandler
from auth_api.consumer.models import BillMessage, BillMessageBody
from auth_api.settings.settings import Settings

logging_config.dictConfig(LOGGING)
logger = logging.getLogger('auth_consumer')
logger.setLevel(logging.INFO)


def start_consuming(con: AbstractBrokerConnector, mh: MessageHandler):
    logger.info('Start consuming...')
    consumer = con.get_consumer()
    for bill_message in consumer:
        logger.info(
            f'Success get message from kafka: {bill_message.title} - {bill_message.body}'
        )
        mh.handle(bill_message)


if __name__ == '__main__':
    settings = Settings()
    message_handler = MessageHandler()
    message_handler.register('bill.paid', add_role_to_user)
    message_handler.register('bill.refunded', delete_user_role)

    fake_messages = [
        BillMessage(
            title='bill.paid',
            body=BillMessageBody(
                user_uuid='3c90a798-30d0-4d52-a421-5840a88fdd64',
                type='subscription',
                item_uuid='6014c570-7ee8-4636-9bca-0415442ca7b6',
            ),
        ),
        BillMessage(
            title='bill.paid',
            body=BillMessageBody(
                user_uuid='6ba9dd3f-0526-4e6c-aa73-e8c45ef110b2',
                type='subscription',
                item_uuid='6014c570-7ee8-4636-9bca-0415442ca7b6',
            ),
        ),
        BillMessage(
            title='bill.refunded',
            body=BillMessageBody(
                user_uuid='3c90a798-30d0-4d52-a421-5840a88fdd64',
                type='subscription',
                item_uuid='6014c570-7ee8-4636-9bca-0415442ca7b6',
            ),
        ),
        BillMessage(
            title='bill.paid',
            body=BillMessageBody(
                user_uuid='3c90a798-30d0-4d52-a421-5840a88fdd64',
                type='subscription',
                item_uuid='6014c570-7ee8-4636-9bca-0415442ca7b6',
            ),
        ),
    ]
    connector = TestConnector(fake_messages, delay=1)
    start_consuming(connector, message_handler)
