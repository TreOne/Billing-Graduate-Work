import uuid

from django.db import models

from billing.models.enums import BillStatus, BillType
from billing.models.mixins import UpdateTimeMixin, UUIDMixin

__all__ = ('Bill',)


class Bill(UUIDMixin, UpdateTimeMixin):
    """Модель для хранения оплат."""

    status = models.CharField(
        verbose_name='Статус оплаты',
        choices=BillStatus.choices,
        max_length=50
    )
    user_uuid = models.UUIDField(
        verbose_name='uuid Пользователя',
        default=uuid.uuid4,
    )
    type = models.CharField(
        verbose_name='Канал уведомления',
        choices=BillType.choices,
        max_length=50
    )
    item_uuid = models.UUIDField(
        verbose_name='uuid Объекта',
        default=uuid.uuid4,
    )
    amount = models.DecimalField(
        verbose_name="Сумма оплаты",
        max_digits=8,
        decimal_places=2,
    )

    class Meta:
        verbose_name = "Оплата"
        verbose_name_plural = "Оплаты"
        db_table = 'bill'

    def __str__(self) -> str:
        return f'{self.pk}: {self.status} - {self.type}'
