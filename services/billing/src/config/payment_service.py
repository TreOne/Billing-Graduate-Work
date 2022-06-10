from django.conf import settings

from utils.payment_system import AbstractPaymentSystem, YooKassaPaymentSystem


def get_payment_service() -> AbstractPaymentSystem:
    return YooKassaPaymentSystem(
        account_id=settings.YOOKASSA_SHOP_ID,
        secret_key=settings.YOOKASSA_SECRET_KEY,
        return_url=settings.YOOKASSA_PAYMENT_RETURN_URL,
    )


payment_system = get_payment_service()
