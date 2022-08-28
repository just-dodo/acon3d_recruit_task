from django.contrib import admin
from core.common_admin import TimeModelAdmin, TimeModelStackedInline
from .models import Merchandise, MerchContent


class MerchContentInline(TimeModelStackedInline):
    model = MerchContent
    fields = (
        "language",
        "title",
        "body",
        "price",
    )


@admin.register(Merchandise)
class MerchandiseAdmin(TimeModelAdmin):
    inlines = [MerchContentInline]


@admin.register(MerchContent)
class MerchContentAdmin(TimeModelAdmin):
    pass
