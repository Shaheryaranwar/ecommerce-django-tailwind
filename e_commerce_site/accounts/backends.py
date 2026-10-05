from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

from .models import Profile


class EmailOrUsernameBackend(ModelBackend):
    """Allow signing in with either username or email address.

    Accounts are only usable once their profile has been approved by an admin.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        User = get_user_model()
        if username is None or password is None:
            return None
        try:
            if "@" in username:
                user = User.objects.get(email__iexact=username)
            else:
                user = User.objects.get(username=username)
        except User.DoesNotExist:
            return None
        if user.check_password(password) and self.user_can_authenticate(user):
            profile = getattr(user, "profile", None)
            if profile is None or profile.status == "approved":
                return user
        return None
