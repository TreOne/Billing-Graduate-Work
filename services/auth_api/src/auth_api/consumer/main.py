from auth_api.consumer.connectors.base import AbstractBrokerConnector
from auth_api.consumer.connectors.kafka_connector import KafkaConnector
from auth_api.consumer.handlers import add_role_to_user, delete_user_role
from auth_api.consumer.message_handler import MessageHandler
from auth_api.settings.settings import Settings


def start_consuming(con: AbstractBrokerConnector, mh: MessageHandler):
    print('Start consuming...')
    consumer = con.get_consumer()
    for bill_message in consumer:
        mh.handle(bill_message)


if __name__ == '__main__':
    settings = Settings()

    message_handler = MessageHandler()
    message_handler.register('bill.paid', add_role_to_user)
    message_handler.register('bill.refunded', delete_user_role)

    connector = KafkaConnector(settings.kafka.host, settings.kafka.topic)
    start_consuming(connector, message_handler)
