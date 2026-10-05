from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_POST

from products.models import Product

from .utils import (
    add_to_wishlist,
    get_wishlist_product_ids,
    remove_from_wishlist,
)


def wishlist_page(request):
    products = Product.objects.none()
    if request.user.is_authenticated:
        products = Product.objects.filter(
            wishlisted_by__user=request.user, is_active=True
        ).select_related("category").prefetch_related("images", "variants")
    else:
        ids = request.session.get("wishlist", [])
        products = Product.objects.filter(id__in=ids, is_active=True).select_related(
            "category"
        ).prefetch_related("images", "variants")

    return render(request, "wishlist/wishlist.html", {"products": products})


@require_POST
def wishlist_toggle(request, product_id):
    product = get_object_or_404(Product, id=product_id, is_active=True)
    ids = get_wishlist_product_ids(request)
    if product.id in ids:
        remove_from_wishlist(request, product)
        added = False
    else:
        add_to_wishlist(request, product)
        added = True

    count = (
        request.user.wishlist_items.count()
        if request.user.is_authenticated
        else len(request.session.get("wishlist", []))
    )
    return JsonResponse(
        {"success": True, "added": added, "count": count}
    )
