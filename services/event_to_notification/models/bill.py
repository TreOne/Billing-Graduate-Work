from uuid import UUID

from models.base import FastJsonModel
from enum import Enum


class BillStatus(str, Enum):
    """Represents default BillStatus."""
    created: str = 'created'
    canceled: str = 'canceled'
    paid: str = 'paid'
    refunded: str = 'refunded '


class BillType(str, Enum):
    subscription: str = 'subscription'
    movie: str = 'movie'


class Bill(FastJsonModel):
    bill_uuid: UUID
    status: BillStatus
    user_uuid: UUID
    type: BillType
    item_uuid: UUID
    amount: int
