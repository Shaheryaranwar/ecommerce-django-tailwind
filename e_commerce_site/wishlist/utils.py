from products.models import Product

from .models import WishlistItem


def get_wishlist_product_ids(request):
    """Return a set of product ids the current visitor has wishlisted."""
    if request.user.is_authenticated:
        return set(
            request.user.wishlist_items.values_list("product_id", flat=True)
        )
    return set(request.session.get("wishlist", []))


def add_to_wishlist(request, product):
    if request.user.is_authenticated:
        WishlistItem.objects.get_or_create(user=request.user, product=product)
    else:
        ids = request.session.get("wishlist", [])
        if product.id not in ids:
            ids.append(product.id)
            request.session["wishlist"] = ids


def remove_from_wishlist(request, product):
    if request.user.is_authenticated:
        WishlistItem.objects.filter(user=request.user, product=product).delete()
    else:
        ids = [i for i in request.session.get("wishlist", []) if i != product.id]
        request.session["wishlist"] = ids


def merge_session_wishlist(request, user):
    """Move any guest wishlist items into the user account on login/registration."""
    ids = request.session.pop("wishlist", [])
    for product_id in ids:
        product = Product.objects.filter(id=product_id).first()
        if product:
            WishlistItem.objects.get_or_create(user=user, product=product)
