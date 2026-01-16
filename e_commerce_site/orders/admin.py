from django.contrib import admin
from .models import Order, OrderItem
# Register your models here.
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    row_id_fields = ['product', 'variant', 'price', 'quantity']

@admin.register(Order) 
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'phone', 'email', 'created_at', 'paid']
    list_filter = ['paid', 'created_at']
    search_fields = ['first_name', 'last_name', 'phone', 'email', 'address', 'city', 'country']
    inlines = [OrderItemInline]