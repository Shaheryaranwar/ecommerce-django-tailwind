from django.contrib import admin

from .models import HeroSlide, SiteSection, StoreSetting


@admin.register(StoreSetting)
class StoreSettingAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            "Branding",
            {
                "fields": (
                    "site_name",
                    "tagline",
                    "logo",
                    "favicon",
                    "primary_color",
                    "secondary_color",
                )
            },
        ),
        (
            "Contact",
            {"fields": ("contact_email", "contact_phone")},
        ),
        (
            "Social links",
            {"fields": ("facebook_url", "instagram_url", "pinterest_url", "youtube_url")},
        ),
        (
            "Announcement bar",
            {"fields": ("announcement_text", "announcement_active")},
        ),
    )

    def has_add_permission(self, request):
        return not StoreSetting.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(HeroSlide)
class HeroSlideAdmin(admin.ModelAdmin):
    list_display = ("heading", "cta_label", "is_active", "sort_order")
    list_editable = ("is_active", "sort_order")
    list_filter = ("is_active",)


@admin.register(SiteSection)
class SiteSectionAdmin(admin.ModelAdmin):
    list_display = ("key", "title", "section_type", "is_active", "sort_order")
    list_editable = ("is_active", "sort_order")
    list_filter = ("is_active", "section_type")
