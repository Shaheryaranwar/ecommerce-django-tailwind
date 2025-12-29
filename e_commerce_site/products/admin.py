from django.contrib import admin
from .models import Category, Supplier, Product, ProductVariant, ProductImage

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "gender", "is_active")
    prepopulated_fields = {"slug": ("name",)}
    list_filter = ("gender", "is_active")
    search_fields = ("name",)
@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ("name", "country", "is_active", "created_at")
    list_filter = ("is_active", "country")
    search_fields = ("name",)


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "category",
        "is_active",
        "is_featured",
        "created_at",
    )

    list_filter = (
        "category",
        "is_active",
        "is_featured",
    )

    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}

    inlines = [
        ProductVariantInline,
        ProductImageInline,
    ]

@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = (
        "product",
        "color",
        "size",
        "price",
        "stock",
        "is_active",
    )

    list_filter = ("color", "size", "is_active")
    search_fields = ("sku",)

