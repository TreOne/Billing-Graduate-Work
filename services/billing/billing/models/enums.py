from enum import Enum

from django.db import models


class BillType(models.TextChoices):
    """Тип оплаты."""

    subscription = "subscription", "Подписка"
    movie = "movie", "Фильм"


class BillStatus(models.TextChoices):
    """Статус оплаты."""

    created = "created", "Создан"
    canceled = "canceled", "Отменен"
    paid = "paid", "Оплачен"
    refunded = "refunded", "Возвращен"


class PaymentStatus(Enum):
    """Статус оплаты."""

    CREATED = 1
    PAID = 2
    CANCELED = 3
    REFUNDED = 4
