from yookassa import Configuration, Payment, Refund
from yookassa.domain.common import ConfirmationType
from yookassa.domain.models import Currency
from yookassa.domain.request import PaymentRequestBuilder
from yookassa.domain.response import PaymentResponse

from billing.models.enums import BillStatus
from payment_system import AbstractPaymentSystem

__all__ = ('YooKassaPaymentSystem',)

from utils.schemas import PaymentParams


class YooKassaPaymentSystem(AbstractPaymentSystem):
    """Реализация платежной системы для ЮKassa.

    docs: https://yookassa.ru/developers/
    repo: https://git.yoomoney.ru/projects/SDK/repos/yookassa-sdk-python/
    """

    def __init__(self, account_id: int, secret_key: str, return_url: str):
        self._account_id = account_id
        self._secret_key = secret_key
        self._return_url = return_url

        Configuration.configure(self._account_id, self._secret_key)

    def create_confirmation_url(self, params: PaymentParams) -> str:
        """Создает ссылку для оплаты."""
        payment = self._create_payment(params)
        confirmation_url = payment.confirmation.confirmation_url
        return confirmation_url

    def make_autopay(self, params: PaymentParams) -> bool:
        """Производит автоматическую оплату."""
        payment = self._create_payment(params)
        payment_status = self._get_status_from_payment(payment)
        is_successful: bool = payment_status == BillStatus.paid
        return is_successful

    def get_payment_status(self, payment_id: str) -> BillStatus:
        """Возвращает статус платежа."""
        payment: PaymentResponse = Payment.find_one(payment_id)
        payment_status = self._get_status_from_payment(payment)
        return payment_status

    def refund_payment(self, payment_id: str, amount: float) -> None:
        Refund.create({
            "amount": {
                "value": str(amount),
                "currency": "RUB"
            },
            "payment_id": payment_id
        })

    def _create_payment(self, params: PaymentParams) -> PaymentResponse:
        """Создает платеж."""
        builder = PaymentRequestBuilder()
        builder.set_amount({'value': params.amount, 'currency': Currency.RUB})

        if params.autopay_id:
            # Автоплатеж
            builder.set_payment_method_id(params.autopay_id)
        else:
            # Требуется подтверждение оплаты пользователем
            builder.set_confirmation(
                {'type': ConfirmationType.REDIRECT, 'return_url': self._return_url}
            )
            if params.save_payment_method:
                builder.set_save_payment_method(True)
                builder.set_payment_method_data({'type': 'bank_card'})

        builder.set_capture(True)  # Автоматический прием поступившего платежа
        builder.set_description(params.description)
        builder.set_metadata({'bill_uuid': params.bill_uuid})

        request = builder.build()
        payment: PaymentResponse = Payment.create(request, idempotency_key=params.bill_uuid)
        return payment

    def _get_status_from_payment(self, payment: PaymentResponse) -> BillStatus:
        """Извлекает статус платежа из объекта PaymentResponse."""
        if payment.refunded_amount and payment.refunded_amount.value:
            return BillStatus.refunded
        payment_status: BillStatus = self.convert_bill_status(payment_status=payment.status)
        return payment_status

    @staticmethod
    def convert_bill_status(payment_status: str) -> BillStatus:
        if payment_status in ('pending', 'waiting_for_capture'):
            return BillStatus.created
        elif payment_status == 'succeeded':
            return BillStatus.paid
        elif payment_status == 'canceled':
            return BillStatus.canceled
        raise ValueError('Failed to determine the payment status.')
