from django.contrib import admin
from core.common_admin import TimeModelAdmin, TimeModelInline
from .models import Merchandise, MerchContent


class MerchContentInline(TimeModelInline):
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
