from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin

from .models import Category


@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin):
    list_display = ("tree_actions", "indented_title", "is_active", "is_featured")
    list_display_links = ("indented_title",)
    list_filter = ("is_active", "is_featured")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}
    list_editable = ("is_active", "is_featured")
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "slug",
                    "parent",
                    "description",
                    "image",
                    "image_url",
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
        ("Display", {"fields": ("is_active", "is_featured", "sort_order")}),
    )
