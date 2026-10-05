from adminsortable2.admin import SortableAdminBase, SortableStackedInline
from django.contrib import admin

from .models import Attribute, AttributeValue, Brand, Product, ProductImage, ProductVariant


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ("name", "country", "is_active")
    list_filter = ("is_active", "country")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


class AttributeValueInline(admin.TabularInline):
    model = AttributeValue
    extra = 1


@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    list_display = ("name", "value_count")
    search_fields = ("name",)
    inlines = [AttributeValueInline]

    @admin.display(description="Values")
    def value_count(self, obj):
        return obj.values.count()


@admin.register(AttributeValue)
class AttributeValueAdmin(admin.ModelAdmin):
    list_display = ("value", "attribute")
    list_filter = ("attribute",)
    search_fields = ("value",)


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1
    filter_horizontal = ("attribute_values",)


class ProductImageInline(SortableStackedInline):
    model = ProductImage
    extra = 1


@admin.register(Product)
class ProductAdmin(SortableAdminBase, admin.ModelAdmin):
    list_display = (
        "name",
        "category",
        "brand",
        "price",
        "in_stock",
        "status",
        "is_active",
        "is_featured",
    )
    list_filter = (
        "category",
        "brand",
        "material",
        "status",
        "is_active",
        "is_featured",
        "is_new",
    )
    search_fields = ("name", "description", "slug", "sku")
    prepopulated_fields = {"slug": ("name",)}
    list_editable = ("is_active", "is_featured")
    inlines = [ProductVariantInline, ProductImageInline]
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "slug",
                    "category",
                    "brand",
                    "sku",
                    "short_description",
                    "description",
                )
            },
        ),
        (
            "Details",
            {
                "fields": (
                    "material",
                    "finish",
                    "dimensions",
                    "assembly_required",
                    "warranty",
                )
            },
        ),
        (
            "SEO",
            {
                "fields": ("meta_title", "meta_description"),
                "classes": ("collapse",),
            },
        ),
        (
            "Visibility & flags",
            {
                "fields": (
                    "status",
                    "is_digital",
                    "is_active",
                    "is_featured",
                    "is_new",
                    "is_bestseller",
                    "is_spotlight",
                )
            },
        ),
    )


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ("product", "name", "sku", "price", "compare_price", "stock", "is_active")
    list_filter = ("is_active",)
    search_fields = ("sku", "product__name")
    filter_horizontal = ("attribute_values",)


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ("product", "is_primary", "sort_order", "has_remote_url")
    list_filter = ("is_primary",)
    search_fields = ("product__name",)

    @admin.display(boolean=True, description="Remote image")
    def has_remote_url(self, obj):
        return bool(obj.image_url)
