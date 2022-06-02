import uuid

from django.db import models

from billing.models.enums import BillStatus, BillType
from billing.models.mixins import UpdateTimeMixin, UUIDMixin

__all__ = ("Bill",)


class Bill(UUIDMixin, UpdateTimeMixin):
    """Модель для хранения Оплат."""

    status = models.CharField(
        verbose_name="Статус оплаты", choices=BillStatus.choices, max_length=50
    )
    user_uuid = models.UUIDField(verbose_name="uuid Пользователя")
    type = models.CharField(
        verbose_name="Канал уведомления", choices=BillType.choices, max_length=50
    )
    item_uuid = models.UUIDField(verbose_name="uuid Объекта")
    amount = models.DecimalField(
        verbose_name="Сумма оплаты",
        max_digits=16,
        decimal_places=2,
    )

    class Meta:
        db_table = "bill"
        verbose_name = "Оплата"
        verbose_name_plural = "Оплаты"

    def __str__(self) -> str:
        return f"{self.pk}: {self.status} - {self.type}"
