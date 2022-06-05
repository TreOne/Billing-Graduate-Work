from django.contrib import admin

from billing.models import UserAutoPay

__all__ = ("UserAutoPayAdmin",)


@admin.register(UserAutoPay)
class UserAutoPayAdmin(admin.ModelAdmin):
    """
    Админка для таблицы Автоплатежей.
    """

    list_display = (
        "id",
        "user_uuid",
        "bill_uuid",
    )
    search_fields = ("id", "user_uuid")
    list_display_links = ("id", "user_uuid")
    fields = (
        "user_uuid",
        "bill_uuid",
    )
    list_per_page = 50
