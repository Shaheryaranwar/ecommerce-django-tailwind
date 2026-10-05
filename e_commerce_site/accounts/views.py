from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import LoginForm, ProfileForm, RegisterForm
from .models import Profile


def register(request):
    if request.user.is_authenticated:
        return redirect("core:home")

    form = RegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(
            request,
            "Your account has been created and is now awaiting approval. "
            "You'll be able to sign in as soon as our team activates it.",
        )
        return redirect("accounts:login")

    return render(request, "accounts/register.html", {"form": form})


@login_required
def profile(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    form = ProfileForm(request.POST or None, instance=profile, user=request.user)

    if request.method == "POST" and form.is_valid():
        form.save(request.user)
        messages.success(request, "Your profile has been updated.")

    return render(
        request,
        "accounts/profile.html",
        {"form": form, "profile": profile},
    )
