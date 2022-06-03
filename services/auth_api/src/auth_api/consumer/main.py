from auth_api.consumer.kafka_consumer import KafkaConnector
from auth_api.consumer.models import Message
from handlers import print_congratulations, send_notification_to_admin, send_notification_to_user
from message_handler import MessageHandler


message_handler = MessageHandler()

message_handler.register('paid', send_notification_to_user)
message_handler.register('cancelled', send_notification_to_admin)

kafka_url = "localhost:9092"
topic = "bill"

consumer = KafkaConnector(kafka_url, topic).init_consumer()


def main():
    for message in consumer:
        title = message.key.decode("utf-8")
        body = message.value
        message = Message(title=title, body=body)
        message_handler.handle(message)

if __name__ == '__main__':
    main()