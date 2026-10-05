from django.contrib import admin

from .models import Cart, CartItem


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("id", "item_count", "total", "updated_at")
    inlines = [CartItemInline]

    @admin.display(description="Total")
    def total(self, obj):
        return f"Rs {obj.get_total_cost():,.0f}"
