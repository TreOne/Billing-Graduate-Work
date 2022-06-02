from django.contrib import admin

from billing.models import Subscription

__all__ = ("SubscriptionAdmin",)


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    """
    Админка для таблицы Подписок.
    """

    list_display = (
        "id",
        "title",
        "price",
        "position",
        "is_active",
        "created_at",
        "updated_at",
    )
    search_fields = (
        "id",
        "title",
    )
    list_display_links = (
        "id",
        "title",
    )
    fields = (
        "title",
        "description",
        "price",
        "position",
        "is_active",
    )
    list_per_page = 50
