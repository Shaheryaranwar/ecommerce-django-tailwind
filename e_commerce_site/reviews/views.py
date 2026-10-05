from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST

from products.models import Product

from .forms import ReviewForm
from .models import Review


@require_POST
@login_required
def submit_review(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)

    existing = Review.objects.filter(product=product, user=request.user).first()
    form = ReviewForm(request.POST, instance=existing)

    if form.is_valid():
        review = form.save(commit=False)
        review.product = product
        review.user = request.user
        review.save()
        messages.success(request, "Thank you! Your review has been published.")

    return redirect(product.get_absolute_url())
