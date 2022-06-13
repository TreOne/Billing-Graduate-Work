from abc import ABC, abstractmethod

from billing.models.enums import BillStatus
from utils.schemas import PaymentParams

__all__ = ('AbstractPaymentSystem',)


class AbstractPaymentSystem(ABC):
    @abstractmethod
    def create_confirmation_url(self, params: PaymentParams) -> str:
        """Создает ссылку для оплаты."""
        raise NotImplementedError

    @abstractmethod
    def make_autopay(self, params: PaymentParams) -> bool:
        """Производит автоматическую оплату."""
        raise NotImplementedError

    @abstractmethod
    def get_payment_status(self, payment_id: str) -> BillStatus:
        """Возвращает статус платежа."""
        raise NotImplementedError

    @abstractmethod
    def refund_payment(self, payment_id: str, amount: float) -> None:
        """Возврат платежа."""
        raise NotImplementedError
