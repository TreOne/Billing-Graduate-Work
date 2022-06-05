from billing.models import UserAutoPay
from billing.repositories import BaseRepository

__all__ = ("UserAutoPayRepository",)


class UserAutoPayRepository(BaseRepository):

    MODEL_CLASS = UserAutoPay

    # def get_
