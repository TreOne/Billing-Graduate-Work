# Generated by Django 3.2.13 on 2022-06-09 00:31

import uuid

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Bill',
            fields=[
                (
                    'id',
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                (
                    'created_at',
                    models.DateTimeField(auto_now_add=True, verbose_name='Дата создания'),
                ),
                (
                    'updated_at',
                    models.DateTimeField(auto_now=True, verbose_name='Дата обновления'),
                ),
                (
                    'status',
                    models.CharField(
                        choices=[
                            ('created', 'Создан'),
                            ('canceled', 'Отменен'),
                            ('paid', 'Оплачен'),
                            ('refunded', 'Возвращен'),
                        ],
                        default='created',
                        max_length=50,
                        verbose_name='Статус оплаты',
                    ),
                ),
                (
                    'user_uuid',
                    models.UUIDField(db_index=True, verbose_name='uuid Пользователя'),
                ),
                (
                    'type',
                    models.CharField(
                        choices=[('subscription', 'Подписка'), ('movie', 'Фильм')],
                        max_length=50,
                        verbose_name='Канал уведомления',
                    ),
                ),
                ('item_uuid', models.UUIDField(verbose_name='uuid Объекта')),
                (
                    'amount',
                    models.DecimalField(
                        decimal_places=2, max_digits=16, verbose_name='Сумма оплаты'
                    ),
                ),
            ],
            options={
                'verbose_name': 'Оплата',
                'verbose_name_plural': 'Оплаты',
                'db_table': 'bill',
            },
        ),
        migrations.CreateModel(
            name='UserAutoPay',
            fields=[
                (
                    'id',
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                (
                    'created_at',
                    models.DateTimeField(auto_now_add=True, verbose_name='Дата создания'),
                ),
                (
                    'user_uuid',
                    models.UUIDField(db_index=True, verbose_name='uuid Пользователя'),
                ),
            ],
            options={
                'verbose_name': 'Автоплатеж',
                'verbose_name_plural': 'Автоплатежи',
                'db_table': 'user_autopay',
            },
        ),
        migrations.AddConstraint(
            model_name='userautopay',
            constraint=models.UniqueConstraint(
                fields=('id', 'user_uuid'), name='unique_user_auth_pay_index'
            ),
        ),
        migrations.AddConstraint(
            model_name='bill',
            constraint=models.UniqueConstraint(
                condition=models.Q(('type', 'movie')),
                fields=('user_uuid', 'item_uuid'),
                name='unique_user_movie_item_index',
            ),
        ),
    ]
