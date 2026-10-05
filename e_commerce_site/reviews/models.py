from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from products.models import Product


class ReviewQuerySet(models.QuerySet):
    def average_for(self, product):
        result = self.filter(product=product).aggregate(
            avg=models.Avg("rating"), count=models.Count("id")
        )
        return {
            "average": result["avg"] or 0,
            "count": result["count"] or 0,
        }


class Review(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="reviews"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    title = models.CharField(max_length=120, blank=True)
    comment = models.TextField()
    is_approved = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = ReviewQuerySet.as_manager()

    class Meta:
        ordering = ("-created_at",)
        unique_together = ("product", "user")

    def __str__(self):
        return f"{self.user} on {self.product} ({self.rating}/5)"

    @property
    def verified_purchase(self):
        if not self.user.is_authenticated:
            return False
        return self.user.orders.filter(
            items__product=self.product, paid=True
        ).exists()
