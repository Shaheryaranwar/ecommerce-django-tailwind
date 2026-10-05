from django.db import models


class StoreSetting(models.Model):
    """Singleton row holding store-wide display settings."""

    site_name = models.CharField(max_length=100, default="Aangan Living")
    tagline = models.CharField(
        max_length=200, default="Handcrafted Furniture & Home Décor", blank=True
    )
    logo = models.ImageField(upload_to="store/", blank=True)
    favicon = models.ImageField(upload_to="store/", blank=True)
    primary_color = models.CharField(max_length=7, default="#3F3A33")
    secondary_color = models.CharField(max_length=7, default="#B4684A")
    contact_email = models.EmailField(default="care@aanganliving.pk")
    contact_phone = models.CharField(max_length=30, default="+92 300 1234567")
    facebook_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    pinterest_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)
    announcement_text = models.CharField(max_length=200, blank=True)
    announcement_active = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Store settings"
        verbose_name_plural = "Store settings"

    def __str__(self):
        return self.site_name

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        return cls.objects.get_or_create(pk=1)[0]


class HeroSlide(models.Model):
    heading = models.CharField(max_length=120)
    subheading = models.TextField(blank=True)
    cta_label = models.CharField(max_length=40, blank=True)
    cta_link = models.CharField(max_length=200, blank=True)
    desktop_image = models.ImageField(upload_to="hero/", blank=True)
    mobile_image = models.ImageField(upload_to="hero/", blank=True)
    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ("sort_order", "id")

    def __str__(self):
        return self.heading


class SiteSection(models.Model):
    """Toggles and orders the homepage content blocks."""

    class SectionType(models.TextChoices):
        HERO = "hero", "Hero Slider"
        FEATURED_CATEGORIES = "featured_categories", "Featured Categories"
        TRENDING_PRODUCTS = "trending_products", "Trending Products"
        SPOTLIGHT = "spotlight", "Single Product Spotlight"
        PROMO = "promo", "Promo Banners"

    key = models.SlugField(unique=True)
    title = models.CharField(max_length=100, blank=True)
    section_type = models.CharField(max_length=30, choices=SectionType.choices)
    sort_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ("sort_order", "id")

    def __str__(self):
        return self.title or self.get_section_type_display()
