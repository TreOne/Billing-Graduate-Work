from utils.payment_system.payment_service import AbstractPayment

__all__ = ('YookassaPayment',)


class YookassaPayment(AbstractPayment):
    def create_payment(self, key: str):
        ...

    def refund_payment(self):
        ...
