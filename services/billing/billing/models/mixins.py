import uuid

from django.db import models

__all__ = ("UUIDMixin", "IsActiveMixin", "CreateTimeMixin", "UpdateTimeMixin")


class UUIDMixin(models.Model):
    """
    Миксин для uuid первичного ключа.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )

    class Meta:
        abstract = True


class IsActiveMixin(models.Model):
    """
    Миксин для флага активности.
    """

    is_active = models.BooleanField(
        verbose_name="Активен",
        default=True,
    )

    class Meta:
        abstract = True


class CreateTimeMixin(models.Model):
    """
    Миксин для времени создания.
    """

    created_at = models.DateTimeField(
        verbose_name="Дата создания",
        auto_now_add=True,
    )

    class Meta:
        abstract = True


class UpdateTimeMixin(CreateTimeMixin):
    """
    Миксин для времени создания и обновления.
    """

    updated_at = models.DateTimeField(
        verbose_name="Дата обновления",
        auto_now=True,
    )

    class Meta:
        abstract = True
