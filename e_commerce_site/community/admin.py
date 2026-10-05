from django.contrib import admin

from .models import Project, ProjectDocument, ProjectImage


class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1


class ProjectDocumentInline(admin.TabularInline):
    model = ProjectDocument
    extra = 1


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "category", "status", "created_at")
    list_filter = ("status", "category")
    search_fields = ("title", "user__username", "user__email")
    inlines = [ProjectImageInline, ProjectDocumentInline]
    actions = ["approve_projects", "reject_projects"]

    @admin.action(description="Approve selected projects")
    def approve_projects(self, request, queryset):
        queryset.update(status="approved")

    @admin.action(description="Reject selected projects")
    def reject_projects(self, request, queryset):
        queryset.update(status="rejected")
