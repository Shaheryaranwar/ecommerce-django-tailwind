from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "order_link",
        "method",
        "status",
        "transaction_id",
        "amount",
        "created_at",
    )

    list_filter = ("method", "status", "created_at")
    search_fields = (
        "transaction_id",
        "order__id",
        "order__email",
        "order__phone",
    )

    readonly_fields = (
        "order",
        "method",
        "amount",
        "transaction_id",
        "created_at",
    )

    ordering = ("-created_at",)

    def order_link(self, obj):
        return f"Order #{obj.order.id}"

    order_link.short_description = "Order"
