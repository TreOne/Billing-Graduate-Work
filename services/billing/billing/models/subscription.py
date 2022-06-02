from django.db import models

from billing.models.mixins import IsActiveMixin, UpdateTimeMixin, UUIDMixin

__all__ = ("Subscription",)


class Subscription(UUIDMixin, IsActiveMixin, UpdateTimeMixin):
    """Модель для хранения Подписок."""

    title = models.CharField(
        verbose_name="Наименование",
        max_length=250,
    )
    description = models.TextField(
        verbose_name="Описание",
        blank=True,
        null=True,
    )
    price = models.DecimalField(
        verbose_name="Цена",
        max_digits=16,
        decimal_places=2,
    )
    position = models.PositiveIntegerField(
        verbose_name="Позиция в списке",
        default=0,
    )

    class Meta:
        db_table = "subscription"
        ordering = ["position"]
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"

    def __str__(self) -> str:
        return f"{self.pk} - {self.title} - {self.price} - {self.is_active}"
