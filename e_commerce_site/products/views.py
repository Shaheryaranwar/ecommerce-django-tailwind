from django.shortcuts import render, get_object_or_404
from .models import Product, Category


def product_list(request, category_slug=None):
    products = Product.objects.filter(is_active=True)
    category = None
    categories = Category.objects.filter(is_active=True)

    if category_slug:
        category = Category.objects.get(slug=category_slug)
        products = products.filter(category=category)

    context = {
        "category": category,
        "categories": categories,  # ✅ THIS WAS MISSING
        "products": products,
    }

    return render(request, "products/product_list.html", context)


def product_detail(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug, is_active=True)

    return render(
        request,
        "products/detail.html",
        {"product": product},
    )
