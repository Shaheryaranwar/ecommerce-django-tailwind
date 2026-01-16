from django.contrib import admin
from .models import Payment
# Register your models here.


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'method', 'amount', 'currency', 'status', 'created_at')
    list_filter = ('method', 'status', 'currency')
    search_fields = ('transaction_id', 'order__id')