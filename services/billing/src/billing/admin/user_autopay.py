from django.contrib import admin

from billing.models import UserAutoPay

__all__ = ("UserAutoPayAdmin",)


@admin.register(UserAutoPay)
class UserAutoPayAdmin(admin.ModelAdmin):
    """
    Админка для таблицы Автоплатеж.
    """

    list_display = (
        "id",
        "user_uuid",
    )
    search_fields = ("id", "user_uuid")
    list_display_links = ("id",)
    fields = (
        "id",
        "user_uuid",
    )
    readonly_fields = (
        "id",
        "user_uuid",
    )
    list_per_page = 50
