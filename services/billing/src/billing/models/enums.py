from django.db import models


class BillType(models.TextChoices):
    """Тип оплаты."""

    subscription = 'subscription', 'Подписка'
    movie = 'movie', 'Фильм'


class BillStatus(models.TextChoices):
    """Статус оплаты."""

    created = 'created', 'Создан'
    canceled = 'canceled', 'Отменен'
    paid = 'paid', 'Оплачен'
    refunded = 'refunded', 'Возвращен'


class YooKassaPaymentStatus(models.TextChoices):
    """
    Основные события из YooKassa.

    docs: https://yookassa.ru/developers/using-api/webhooks
    """

    payment_succeeded = 'payment.succeeded', 'Успешен'
    payment_canceled = 'payment.canceled', 'Отменен'
    refund_succeeded = 'refund.succeeded', 'Возвращен'
