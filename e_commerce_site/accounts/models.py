from django.conf import settings
from django.db import models


class Profile(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending Approval"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile"
    )
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="approved"
    )
    phone = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, default="Pakistan", blank=True)
    postal_code = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"Profile of {self.user}"
