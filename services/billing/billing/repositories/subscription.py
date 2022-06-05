from billing.models import Subscription
from billing.repositories import BaseRepository

__all__ = ("SubscriptionRepository",)


class SubscriptionRepository(BaseRepository):
    MODEL_CLASS = Subscription
