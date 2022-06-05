from typing import Optional

from utils.schemas import FastJsonModel


class PaymentParams(FastJsonModel):
    """Параметры для создания платежа."""

    bill_uuid: str
    amount: float
    description: str
    save_payment_method: bool = False  # Сохранить платежные данные для автоплатежей?
    autopay_id: Optional[str] = None  # Идентификатор для проведения автоплатежа.
