from django.contrib import admin

from billing.models import Bill, Subscription


@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    """
    Админка для таблицы Оплат.
    """

    ...


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    """
    Админка для таблицы Подписок.
    """

    ...
