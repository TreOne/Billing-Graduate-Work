from django.contrib import admin

from billing.models import Bill

__all__ = ('BillAdmin',)


@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    """
    Админка для таблицы Оплат.
    """

    list_display = (
        'id',
        'status',
        'type',
        'amount',
        'created_at',
        'updated_at',
    )
    search_fields = ('id',)
    list_display_links = ('id',)
    fields = (
        'status',
        'user_uuid',
        'type',
        'item_uuid',
        'amount',
        'payment_uuid',
    )
    list_per_page = 50
