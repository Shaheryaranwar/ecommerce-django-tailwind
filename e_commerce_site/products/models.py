from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse
from django_ckeditor_5.fields import CKEditor5Field

from categories.models import Category


class Brand(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    country = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Attribute(models.Model):
    """A product attribute such as Color or Size."""

    name = models.CharField(max_length=60, unique=True)

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name


class AttributeValue(models.Model):
    """A concrete value of an attribute, e.g. Color -> Walnut."""

    attribute = models.ForeignKey(
        Attribute, on_delete=models.CASCADE, related_name="values"
    )
    value = models.CharField(max_length=100)

    class Meta:
        ordering = ("attribute__name", "value")
        unique_together = ("attribute", "value")

    def __str__(self):
        return f"{self.attribute.name}: {self.value}"


class Product(models.Model):
    MATERIAL_CHOICES = [
        ("wood", "Wood"),
        ("fabric", "Fabric"),
        ("leather", "Leather"),
        ("metal", "Metal"),
        ("glass", "Glass"),
        ("marble", "Marble"),
        ("rattan", "Rattan"),
        ("velvet", "Velvet"),
        ("mixed", "Mixed Materials"),
    ]
    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("published", "Published"),
    ]

    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    sku = models.CharField(max_length=50, unique=True, blank=True, null=True)
    brand = models.ForeignKey(
        Brand, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="products",
    )
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="products"
    )
    short_description = models.CharField(
        max_length=255,
        blank=True,
        help_text="One-line summary shown on product cards.",
    )
    description = CKEditor5Field()
    material = models.CharField(max_length=20, choices=MATERIAL_CHOICES, blank=True)
    finish = models.CharField(max_length=100, blank=True)
    dimensions = models.CharField(
        max_length=120, blank=True, help_text='e.g. 84" W x 36" D x 30" H'
    )
    assembly_required = models.BooleanField(default=False)
    warranty = models.CharField(max_length=100, blank=True)

    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="published"
    )
    is_digital = models.BooleanField(
        default=False, help_text="Digital products skip shipping."
    )
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    is_new = models.BooleanField(default=False, help_text="Show 'New' badge.")
    is_bestseller = models.BooleanField(default=False, help_text="Show 'Best Seller' badge.")
    is_spotlight = models.BooleanField(
        default=False,
        help_text="Feature alone in the home page 'Single Product Spotlight' section.",
    )
    meta_title = models.CharField(max_length=120, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("products:product_detail", args=[self.slug])

    @property
    def primary_image(self):
        return self.images.filter(is_primary=True).first() or self.images.first()

    @property
    def price(self):
        variant = self.variants.filter(is_active=True).first()
        return variant.price if variant else None

    @property
    def compare_price(self):
        variant = self.variants.filter(is_active=True).first()
        return variant.compare_price if variant else None

    @property
    def discount_percentage(self):
        variant = self.variants.filter(is_active=True).first()
        return variant.discount_percentage() if variant else 0

    @property
    def in_stock(self):
        return self.variants.filter(is_active=True, stock__gt=0).exists()

    @property
    def average_rating(self):
        from reviews.models import Review

        return Review.objects.average_for(self)


class ProductVariant(models.Model):
    """A finish / size option with its own price, SKU and stock."""

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="variants"
    )
    name = models.CharField(max_length=100, help_text='e.g. "Walnut", "Teak", "Oak"')
    sku = models.CharField(max_length=50, unique=True)
    attribute_values = models.ManyToManyField(
        AttributeValue, blank=True, related_name="variants"
    )
    image = models.ImageField(upload_to="products/variants/", blank=True)
    price = models.DecimalField(
        max_digits=12, decimal_places=2, validators=[MinValueValidator(0)]
    )
    compare_price = models.DecimalField(
        max_digits=12, decimal_places=2, blank=True, null=True,
        help_text="Original price, shown struck-through on sale.",
    )
    stock = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ("price",)

    def __str__(self):
        return f"{self.product.name} — {self.name}"

    def in_stock(self):
        return self.stock > 0

    def discount_percentage(self):
        if self.compare_price and self.compare_price > self.price:
            return round(((self.compare_price - self.price) / self.compare_price) * 100)
        return 0


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(upload_to="products/", blank=True, null=True)
    image_url = models.URLField(
        blank=True, help_text="Remote placeholder image used during development."
    )
    alt_text = models.CharField(max_length=200, blank=True)
    is_primary = models.BooleanField(default=False)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ("sort_order", "id")

    def __str__(self):
        return f"Image for {self.product.name}"

    @property
    def display_url(self):
        return self.image_url or (self.image.url if self.image else "")
