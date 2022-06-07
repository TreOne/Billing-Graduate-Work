from kafka import KafkaConsumer

from auth_api.consumer.kafka_consumer import KafkaConnector
from auth_api.consumer.models import Message, BodyMessage
from auth_api.settings.settings import Settings
from handlers import add_role_to_user, delete_user_role
from message_handler import MessageHandler


def start_consuming(cons: KafkaConsumer, mh: MessageHandler):
    for message in cons:
        title = message.key.decode("utf-8")
        body = message.value
        message = Message(title=title, body=BodyMessage(**body))
        mh.handle(message)


if __name__ == '__main__':
    settings = Settings()

    message_handler = MessageHandler()
    message_handler.register('bill.paid', add_role_to_user)
    message_handler.register('bill.refunded', delete_user_role)

    consumer = KafkaConnector(settings.kafka.kafka_url, settings.kafka.topic).get_consumer()
    start_consuming(consumer, message_handler)
