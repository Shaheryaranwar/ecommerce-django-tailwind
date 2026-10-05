from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth.models import User

from .models import Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False


class ProfileStatusFilter(admin.SimpleListFilter):
    title = "account status"
    parameter_name = "profile_status"

    def lookups(self, request, model_admin):
        return Profile.STATUS_CHOICES

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(profile__status=self.value())
        return queryset


class UserAdmin(DjangoUserAdmin):
    inlines = [ProfileInline]
    list_filter = DjangoUserAdmin.list_filter + (ProfileStatusFilter,)
    actions = ["approve_users", "reject_users"]

    def _set_status(self, request, queryset, status):
        count = 0
        for user in queryset:
            profile, _ = Profile.objects.get_or_create(user=user)
            if profile.status != status:
                profile.status = status
                profile.save(update_fields=["status"])
                count += 1
        self.message_user(
            request, f"{count} account(s) set to “{status}”.", messages.SUCCESS
        )

    @admin.action(description="Approve selected accounts")
    def approve_users(self, request, queryset):
        self._set_status(request, queryset, "approved")

    @admin.action(description="Reject selected accounts")
    def reject_users(self, request, queryset):
        self._set_status(request, queryset, "rejected")

    def get_list_display(self, request):
        return super().get_list_display(request) + ("profile_status",)

    @admin.display(description="Account status")
    def profile_status(self, obj):
        return getattr(getattr(obj, "profile", None), "status", "approved")


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
