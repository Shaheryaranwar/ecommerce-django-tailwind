from django.contrib import admin

from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("variant_name", "sku")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "first_name",
        "last_name",
        "phone",
        "city",
        "status",
        "paid",
        "total",
        "created_at",
    )
    list_filter = ("status", "paid", "created_at", "city")
    search_fields = ("first_name", "last_name", "phone", "email", "address")
    inlines = [OrderItemInline]
    date_hierarchy = "created_at"

    @admin.display(description="Total")
    def total(self, obj):
        return f"Rs {obj.get_total_cost():,.0f}"
