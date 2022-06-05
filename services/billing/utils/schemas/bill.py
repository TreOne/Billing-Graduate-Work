from utils.schemas import FastJsonModel


class BillSchema(FastJsonModel):
    """Параметры для сериализаций Оплаты."""

    bill_uuid: str
    status: str
    user_uuid: str
    type: str
    item_uuid: str
    amount: float
