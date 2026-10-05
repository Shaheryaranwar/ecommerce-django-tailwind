from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from .models import Profile


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=50, required=False)
    last_name = forms.CharField(max_length=50, required=False)

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"].lower()
        if commit:
            user.save()
            Profile.objects.update_or_create(
                user=user, defaults={"status": "pending"}
            )
        return user


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Username or email"})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Password"})
    )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")
        if not username or not password:
            return cleaned_data

        if self.user_cache is not None:
            status = getattr(getattr(self.user_cache, "profile", None), "status", "approved")
            if status != "approved":
                self.user_cache = None
                raise self._status_error(status)
            return cleaned_data

        try:
            if "@" in username:
                user = get_user_model().objects.get(email__iexact=username)
            else:
                user = get_user_model().objects.get(username=username)
        except get_user_model().DoesNotExist:
            return cleaned_data
        if user.check_password(password):
            status = getattr(getattr(user, "profile", None), "status", "approved")
            if status != "approved":
                raise self._status_error(status)
        return cleaned_data

    @staticmethod
    def _status_error(status):
        if status == "pending":
            return forms.ValidationError(
                "Your account is awaiting approval. We'll email you as soon as it's activated.",
                code="account_pending",
            )
        return forms.ValidationError(
            "Your account application was declined. Contact care@aanganliving.pk if you think this is a mistake.",
            code="account_rejected",
        )


class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50, required=False)
    last_name = forms.CharField(max_length=50, required=False)
    email = forms.EmailField(required=True)

    class Meta:
        model = Profile
        fields = ("phone", "address", "city", "country", "postal_code")
        widgets = {
            "phone": forms.TextInput(attrs={"placeholder": "03XX XXXXXXX"}),
            "address": forms.TextInput(attrs={"placeholder": "House, street, area"}),
            "city": forms.TextInput(attrs={"placeholder": "City"}),
            "country": forms.TextInput(attrs={"placeholder": "Pakistan"}),
            "postal_code": forms.TextInput(attrs={"placeholder": "Postal code"}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")
        super().__init__(*args, **kwargs)
        self.fields["first_name"].initial = user.first_name
        self.fields["last_name"].initial = user.last_name
        self.fields["email"].initial = user.email

    def save(self, user):
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"].lower()
        user.save()
        return super().save()
