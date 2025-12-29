from django.contrib import admin
from django import forms
from .models import Category, Supplier, Product

PRODUCT_TYPE_BY_CATEGORY = {
    'men-clothing': [
        'mens_tshirt', 'mens_shirt', 'mens_trouser',
        'mens_jeans', 'mens_kurta', 'mens_shalwar',
        'mens_waistcoat', 'mens_blazer', 'mens_suit',
        'mens_hoodie', 'mens_jacket', 'mens_coat',
        'mens_short', 'mens_shoes', 'mens_sweater',
    ],
    'women-clothing': [
        'womens_kurta', 'womens_suit', 'womens_dress',
        'womens_abaya', 'womens_hoodie', 'womens_trouser',
        'womens_jeans', 'womens_blouse', 'womens_shawl',
        'womens_jacket', 'womens_coat', 'womens_skirt',
        'womens_sweater', 'womens_shoes',
    ],
    'kids-clothing': [
        'kids_kurta', 'kids_tshirt', 'kids_trouser',
        'kids_dress', 'kids_traditional', 'kids_jeans',
        'kids_hoodie', 'kids_jacket', 'kids_coat',
        'kids_shoes',
    ],
}

class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance.pk and self.instance.category:
            slug = self.instance.category.slug
            allowed = PRODUCT_TYPE_BY_CATEGORY.get(slug)

            if allowed:
                self.fields['product_type'].choices = [
                    c for c in self.fields['product_type'].choices
                    if c[0] in allowed
                ]

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_active')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm

    class Media:
        js = ('admin/js/product_admin.js',)

    list_display = (
        'name', 'price', 'category',
        'product_type', 'size',
        'stock_quantity', 'is_active',
        'image',
    )

    list_filter = (
        'category', 'product_type',
        'size', 'color',
        'season', 'occasion',
        'is_active',
    )

    search_fields = ('name', 'sku')
    prepopulated_fields = {'slug': ('name',)}

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'category', 'product_type',
                       'price', 'compare_price', 'cost_price', 'sku', 'image')
        }),
        ('Attributes', {
            'fields': ('fabric_type', 'size', 'color',
                       'season', 'occasion')
        }),
        ('Measurements', {
            'fields': ('length', 'chest_width',
                       'waist_width', 'shoulder_width')
        }),
        ('Inventory & Status', {
            'fields': ('stock_quantity',
                       'is_active', 'is_featured')
        }),
    )