import uuid

from django.db import models

from billing.models.enums import BillStatus, BillType
from billing.models.mixins import UpdateTimeMixin, UUIDMixin

__all__ = ('Subscribe',)


class Subscribe(UUIDMixin, UpdateTimeMixin):
    """Модель для хранения шаблона сообщения."""

    title = models.CharField(
        verbose_name='Наименование', max_length=250,
    )

    def __str__(self) -> str:
        return f'{self.pk}'

    class Meta:
        db_table = 'subscribe'

