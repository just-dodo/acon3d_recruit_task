from django.contrib import admin
from core.common_admin import (
    TimeModelAdmin,
    TimeModelTabularInline,
    TimeModelStackedInline,
)
from .models import Merchandise, MerchContent, Purchase


class MerchContentInline(TimeModelStackedInline):
    model = MerchContent
    fields = (
        "language",
        "title",
        "body",
        "price",
    )


class PurchaseInline(TimeModelTabularInline):
    model = Purchase
    fields = (
        "user",
        "language",
        "price",
    )


@admin.register(Merchandise)
class MerchandiseAdmin(TimeModelAdmin):
    inlines = [MerchContentInline, PurchaseInline]
    pass


@admin.register(MerchContent)
class MerchContentAdmin(TimeModelAdmin):
    pass


@admin.register(Purchase)
class PurchaseAdmin(TimeModelAdmin):
    pass
