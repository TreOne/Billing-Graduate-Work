from handlers import send_notification_to_admin, send_notification_to_user
from message_handler import MessageHandler


message_handler = None


def main():
    for message in messages:
        message_handler.handle(message.title, message.body)


if __name__ == '__main__':
    message_handler = MessageHandler()
    message_handler.register('bill.created', send_notification_to_user)
    message_handler.register('bill.refunded', send_notification_to_user)
    message_handler.register('bill.refunded', send_notification_to_admin)
    main()
