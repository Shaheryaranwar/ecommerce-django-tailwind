from django.db import models
from django.urls import reverse
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel


class Category(MPTTModel):
    """Furniture category hierarchy managed with django-mptt."""

    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    parent = TreeForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="children",
        null=True,
        blank=True,
    )
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="categories/", blank=True)
    image_url = models.URLField(
        blank=True,
        help_text="Remote placeholder image used during development.",
    )
    meta_title = models.CharField(
        max_length=120, blank=True, help_text="Optional SEO title for this category page."
    )
    meta_description = models.CharField(
        max_length=160, blank=True, help_text="Optional SEO description for this category page."
    )
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(
        default=False,
        help_text="Show on the home page category grid.",
    )
    sort_order = models.PositiveIntegerField(default=0)

    class MPTTMeta:
        order_insertion_by = ("sort_order", "name")

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    @property
    def display_image(self):
        return self.image_url or (self.image.url if self.image else "")

    def get_absolute_url(self):
        return reverse("products:category_detail", args=[self.slug])

    def descendant_ids(self):
        return list(
            self.get_descendants(include_self=True).values_list("id", flat=True)
        )
