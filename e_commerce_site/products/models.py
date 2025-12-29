from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator
# category model
class Category(models.Model):
    GENDER_CHOICES = [
        ("men", "Men"),
        ("women", "Women"),
        ("kids", "Kids"),
        ("unisex", "Unisex"),
    ]

    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to="categories/", blank=True)
    gender = models.CharField(
        max_length=10, choices=GENDER_CHOICES, default="unisex"
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("products:category_detail", args=[self.slug])
# Supplier model
class Supplier(models.Model):
    name = models.CharField(max_length=200)
    contact_email = models.EmailField(blank=True)
    phone = models.CharField(max_length=50, blank=True)
    country = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
# Product model (DESIGN / DESCRIPTION ONLY)
class Product(models.Model):
    FABRIC_CHOICES = [
        ("cotton", "Cotton"),
        ("linen", "Linen"),
        ("silk", "Silk"),
        ("denim", "Denim"),
        ("chiffon", "Chiffon"),
        ("wool", "Wool"),
    ]

    SEASON_CHOICES = [
        ("summer", "Summer"),
        ("winter", "Winter"),
        ("all", "All Season"),
    ]

    OCCASION_CHOICES = [
        ("casual", "Casual"),
        ("formal", "Formal"),
        ("party", "Party"),
        ("wedding", "Wedding"),
        ("eid", "Eid"),
    ]

    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()

    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="products"
    )
    supplier = models.ForeignKey(
        Supplier, on_delete=models.SET_NULL, null=True, blank=True
    )

    fabric = models.CharField(
        max_length=20, choices=FABRIC_CHOICES, blank=True
    )
    season = models.CharField(
        max_length=10, choices=SEASON_CHOICES, default="all"
    )
    occasion = models.CharField(
        max_length=20, choices=OCCASION_CHOICES, default="casual"
    )

    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("products:product_detail", kwargs={'id':self.id , 'slug':self.slug})

#PRODUCT VARIANT (THIS IS THE MOST IMPORTANT MODEL)
class ProductVariant(models.Model):
    SIZE_CHOICES = [
        ("xs", "XS"),
        ("s", "S"),
        ("m", "M"),
        ("l", "L"),
        ("xl", "XL"),
        ("xxl", "XXL"),
    ]

    COLOR_CHOICES = [
        ("white", "White"),
        ("black", "Black"),
        ("blue", "Blue"),
        ("red", "Red"),
        ("green", "Green"),
        ("gray", "Gray"),
    ]

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="variants"
    )

    size = models.CharField(max_length=10, choices=SIZE_CHOICES)
    color = models.CharField(max_length=20, choices=COLOR_CHOICES)

    sku = models.CharField(max_length=50, unique=True)

    price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)]
    )
    compare_price = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    cost_price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)]
    )

    stock = models.PositiveIntegerField(default=0)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("product", "size", "color")

    def __str__(self):
        return f"{self.product.name} - {self.color} - {self.size}"

    def in_stock(self):
        return self.stock > 0

    def discount_percentage(self):
        if self.compare_price and self.compare_price > self.price:
            return int(
                ((self.compare_price - self.price) / self.compare_price) * 100
            )
        return 0
# Product Image model
class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(upload_to="products",blank=True, null=True)
    alt_text = models.CharField(max_length=200, blank=True)
    is_primary = models.BooleanField(default=False)
    color = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"Image for {self.product.name}"

