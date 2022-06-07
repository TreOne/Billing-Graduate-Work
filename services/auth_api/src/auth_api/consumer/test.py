from auth_api.consumer.connectors.base import AbstractBrokerConnector
from auth_api.consumer.connectors.test_connector import TestConnector
from auth_api.consumer.handlers import add_role_to_user, delete_user_role
from auth_api.consumer.message_handler import MessageHandler
from auth_api.consumer.models import BillMessage, BillMessageBody
from auth_api.settings.settings import Settings


def start_consuming(con: AbstractBrokerConnector, mh: MessageHandler):
    consumer = con.get_consumer()
    for bill_message in consumer:
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
                user_uuid='969c176c-6ab9-4997-b186-b6c999992dcc',
                type='subscription',
                item_uuid='6014c570-7ee8-4636-9bca-0415442ca7b6',
            ),
        ),
        BillMessage(
            title='bill.paid',
            body=BillMessageBody(
                user_uuid='b4589279-3602-414e-ab93-dbe1185106e3',
                type='subscription',
                item_uuid='6014c570-7ee8-4636-9bca-0415442ca7b6',
            ),
        ),
        BillMessage(
            title='bill.refunded',
            body=BillMessageBody(
                user_uuid='969c176c-6ab9-4997-b186-b6c999992dcc',
                type='subscription',
                item_uuid='6014c570-7ee8-4636-9bca-0415442ca7b6',
            ),
        ),
    ]
    connector = TestConnector(fake_messages, delay=10)
    start_consuming(connector, message_handler)
