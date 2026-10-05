from django.conf import settings
from django.db import models
from django.urls import reverse

PROJECT_CATEGORIES = [
    ("makeover", "Room Makeover"),
    ("restoration", "Restoration"),
    ("diy", "DIY Build"),
    ("styling", "Styling & Decor"),
    ("workshop", "Workshop Project"),
]


class Project(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending Review"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="projects",
    )
    title = models.CharField(max_length=120)
    category = models.CharField(
        max_length=20, choices=PROJECT_CATEGORIES, default="styling"
    )
    description = models.TextField()
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="pending", db_index=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("community:project_detail", args=[self.pk])

    @property
    def cover_image(self):
        return self.images.first()


class ProjectImage(models.Model):
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(upload_to="community/projects/%Y/%m/")
    caption = models.CharField(max_length=200, blank=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "id"]

    def __str__(self):
        return f"{self.project.title} — image {self.pk}"


class ProjectDocument(models.Model):
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="documents"
    )
    title = models.CharField(max_length=120)
    file = models.FileField(upload_to="community/documents/%Y/%m/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
