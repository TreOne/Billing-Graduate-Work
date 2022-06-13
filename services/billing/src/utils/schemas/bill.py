from utils.schemas import FastJsonModel

__all__ = ('BillSchema', 'BillBaseSchema')


class BillBaseSchema(FastJsonModel):
    """Параметры для сериализаций запроса на Оплату."""

    user_uuid: str
    type: str
    item_uuid: str


class BillSchema(BillBaseSchema):
    """Параметры для сериализаций Оплаты."""

    bill_uuid: str
    status: str
    amount: float
