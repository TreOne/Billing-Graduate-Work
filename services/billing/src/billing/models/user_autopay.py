from django.db import models

from billing.models.mixins import CreateTimeMixin, UUIDMixin

__all__ = ('UserAutoPay',)


class UserAutoPay(UUIDMixin, CreateTimeMixin):
    """Модель для хранения Автоплатежей пользователя."""

    user_uuid = models.UUIDField(verbose_name='uuid Пользователя', db_index=True)

    class Meta:
        db_table = 'user_autopay'
        verbose_name = 'Автоплатеж'
        verbose_name_plural = 'Автоплатежи'
        constraints = [
            models.UniqueConstraint(
                fields=['id', 'user_uuid'], name='unique_user_auth_pay_index',
            )
        ]

    def __str__(self) -> str:
        return f'{self.pk}: {self.user_uuid}'
