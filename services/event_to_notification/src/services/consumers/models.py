from dataclasses import dataclass


@dataclass
class BillMessage:
    """Схема сообщения из очереди Bills."""
    bill_uuid: str
    status: str
    user_uuid: str
    type: str
    item_uuid: str
    amount: float
