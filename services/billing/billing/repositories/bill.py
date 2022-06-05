from billing.models import Bill
from billing.repositories import BaseRepository

__all__ = ("BillRepository",)


class BillRepository(BaseRepository):

    MODEL_CLASS = Bill
