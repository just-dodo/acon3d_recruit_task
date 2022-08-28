from django.contrib import admin

class TimeModelAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "created_at",
        "updated_at",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
        "deleted_at",
    )

class TimeModelTabularInline(admin.TabularInline):
    extra = 0
    readonly_fields = (
        "created_at",
        "updated_at",
        "deleted_at",
    )
class TimeModelStackedInline(admin.StackedInline):
    extra = 0
    readonly_fields = (
        "created_at",
        "updated_at",
        "deleted_at",
    )
