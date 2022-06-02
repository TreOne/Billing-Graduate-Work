from django.contrib import admin
from billing.models import Bill, Subscribe


@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    """Админка для модели Bill."""
    ...


@admin.register(Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    """Админка для модели Subscribe."""
    ...
