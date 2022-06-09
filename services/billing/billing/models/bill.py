from django.db import models
from django.db.models import Q

from billing.models.enums import BillStatus, BillType
from billing.models.mixins import UpdateTimeMixin, UUIDMixin

__all__ = ("Bill",)

from config.kafka_producer import producer
from utils.schemas.bill import BillSchema


class Bill(UUIDMixin, UpdateTimeMixin):
    """Модель для хранения Оплат."""

    status = models.CharField(
        verbose_name="Статус оплаты",
        choices=BillStatus.choices,
        max_length=50,
        default=BillStatus.created,
    )
    user_uuid = models.UUIDField(verbose_name="uuid Пользователя", db_index=True)
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
        constraints = [
            models.UniqueConstraint(
                fields=["user_uuid", "item_uuid"],
                condition=Q(type=BillType.movie),
                name="unique_user_movie_item_index",
            )
        ]

    def __str__(self) -> str:
        return f"{self.pk}: {self.status} - {self.type}"

    def save(self, *args, **kwargs):
        """
        Расширение метода сохранения, для отправки сообщений в Kafka.
        """
        # before save
        super().save(*args, **kwargs)
        # after save
        data = BillSchema(
            **{
                "bill_uuid": str(self.pk),
                "status": f"bill.{self.status}",
                "user_uuid": str(self.user_uuid),
                "type": self.type,
                "item_uuid": str(self.item_uuid),
                "amount": float(self.amount),
            }
        )
        producer.produce("default", data.json())
        producer.flush()
