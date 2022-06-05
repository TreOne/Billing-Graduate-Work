# Generated by Django 3.2.13 on 2022-06-02 15:34

import uuid

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Bill",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Дата создания"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="Дата обновления"),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("created", "Создан"),
                            ("canceled", "Отменен"),
                            ("paid", "Оплачен"),
                            ("refunded", "Возвращен"),
                        ],
                        max_length=50,
                        verbose_name="Статус оплаты",
                    ),
                ),
                (
                    "user_uuid",
                    models.UUIDField(
                        default=uuid.uuid4, verbose_name="uuid Пользователя"
                    ),
                ),
                (
                    "type",
                    models.CharField(
                        choices=[("subscription", "Подписка"), ("movie", "Фильм")],
                        max_length=50,
                        verbose_name="Канал уведомления",
                    ),
                ),
                (
                    "item_uuid",
                    models.UUIDField(default=uuid.uuid4, verbose_name="uuid Объекта"),
                ),
                (
                    "amount",
                    models.DecimalField(
                        decimal_places=2, max_digits=16, verbose_name="Сумма оплаты"
                    ),
                ),
            ],
            options={
                "verbose_name": "Оплата",
                "verbose_name_plural": "Оплаты",
                "db_table": "bill",
            },
        ),
        migrations.CreateModel(
            name="Subscription",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(default=True, verbose_name="Активен"),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Дата создания"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="Дата обновления"),
                ),
                (
                    "title",
                    models.CharField(max_length=250, verbose_name="Наименование"),
                ),
                (
                    "description",
                    models.TextField(blank=True, null=True, verbose_name="Описание"),
                ),
                (
                    "price",
                    models.DecimalField(
                        decimal_places=2, max_digits=16, verbose_name="Цена"
                    ),
                ),
                (
                    "position",
                    models.PositiveIntegerField(
                        default=0, verbose_name="Позиция в списке"
                    ),
                ),
            ],
            options={
                "verbose_name": "Подписка",
                "verbose_name_plural": "Подписки",
                "db_table": "subscription",
                "ordering": ["position"],
            },
        ),
    ]