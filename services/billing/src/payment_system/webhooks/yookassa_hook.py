from django.conf import settings
from yookassa import Configuration, Webhook

from billing.models.enums import YooKassaPaymentStatus

Configuration.configure_auth_token('<Bearer Token>')

yookassa_webhook = Webhook()

yookassa_webhook.add(
    {'event': YooKassaPaymentStatus.payment_succeeded, 'url': settings.YOOKASSA_NOTIFICATION_URL, }
)

yookassa_webhook.add(
    {'event': YooKassaPaymentStatus.payment_canceled, 'url': settings.YOOKASSA_NOTIFICATION_URL, }
)

yookassa_webhook.add(
    {'event': YooKassaPaymentStatus.refund_succeeded, 'url': settings.YOOKASSA_REFUND_NOTIFICATION_URL, }
)
