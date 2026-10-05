from django.contrib import admin

from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "method", "status", "amount", "transaction_id", "created_at")
    list_filter = ("method", "status", "created_at")
    search_fields = ("order__first_name", "order__email", "transaction_id")
    date_hierarchy = "created_at"
