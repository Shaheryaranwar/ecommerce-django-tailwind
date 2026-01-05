from django.shortcuts import render, get_object_or_404
from .models import Product, Category


def product_list(request, category_slug=None):
    products = Product.objects.filter(is_active=True)
    category = None
    categories = Category.objects.filter(is_active=True)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    return render(
        request,
        "products/product_list.html",
        {
            "category": category,
            "categories": categories,
            "products": products,
        },
    )


def product_detail(request, id, product_slug):
    product = get_object_or_404(
        Product,
        id=id,
        slug=product_slug,
        is_active=True
    )

    return render(
        request,
        "products/detail.html",
        {"product": product},
    )
