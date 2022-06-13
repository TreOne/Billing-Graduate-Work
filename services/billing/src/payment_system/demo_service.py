from billing.models.enums import BillStatus
from payment_system import AbstractPaymentSystem
from utils.schemas import PaymentParams

__all__ = ('TestPaymentSystem',)


class TestPaymentSystem(AbstractPaymentSystem):
    """Реализация платежной системы для проведения тестирования (без проведения реальных платежей)."""

    def create_confirmation_url(self, params: PaymentParams) -> str:
        """Создает ссылку для оплаты."""
        return 'https://example.com'

    def make_autopay(self, params: PaymentParams) -> bool:
        """Производит автоматическую оплату."""
        return True

    def get_payment_status(self, payment_id: str) -> BillStatus:
        """Возвращает статус платежа."""
        return BillStatus.paid

    def refund_payment(self, payment_id: str, amount: float) -> None:
        """Возврат платежа."""
        return None
