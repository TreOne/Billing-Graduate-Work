from models.base import FastJsonModel


class IncomingBill(FastJsonModel):
    """Message to send model ."""

    bill_uuid: str
    status: str
    user_uuid: str
    type: str
    item_uuid: str
    amount: float
