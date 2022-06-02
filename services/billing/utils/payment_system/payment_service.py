from abc import ABC, abstractmethod
from typing import Optional


class AbstractPayment(ABC):
    def __init__(self, cache_instance):
        self.cache = cache_instance

    @abstractmethod
    def create_payment(self, key: str):
        pass

    @abstractmethod
    def refund_payment(self):
        pass


payment_service: Optional[AbstractPayment] = None


def get_payment_service() -> AbstractPayment:
    return payment_service
