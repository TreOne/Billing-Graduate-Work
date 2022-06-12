from django.conf import settings
from yookassa import Configuration, Webhook

Configuration.configure_auth_token('<Bearer Token>')

yookassa_webhook = Webhook()

yookassa_webhook.add(
    {'event': 'payment.succeeded', 'url': settings.YOOKASSA_NOTIFICATION_URL, }
)

yookassa_webhook.add(
    {'event': 'payment.canceled', 'url': settings.YOOKASSA_NOTIFICATION_URL, }
)
