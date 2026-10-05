from categories.models import Category
from cart.models import Cart
from core.models import StoreSetting


def _cart_data(request):
    cart_id = request.session.get("cart_id")
    if not cart_id:
        return {"cart_count": 0, "cart_subtotal": 0}
    cart = Cart.objects.filter(id=cart_id).first()
    if not cart:
        return {"cart_count": 0, "cart_subtotal": 0}
    return {
        "cart_count": cart.item_count,
        "cart_subtotal": cart.get_total_cost(),
    }


def _wishlist_data(request):
    if request.user.is_authenticated:
        ids = set(request.user.wishlist_items.values_list("product_id", flat=True))
    else:
        ids = set(request.session.get("wishlist", []))
    return {"wishlist_count": len(ids), "wishlist_ids": ids}


def store(request):
    nav_categories = (
        Category.objects.filter(is_active=True, parent__isnull=True)
        .prefetch_related("children")
        .order_by("sort_order", "name")
    )
    settings = StoreSetting.load()
    return {
        "nav_categories": nav_categories,
        "store_name": settings.site_name or "Aangan Living",
        "store_phone": settings.contact_phone or "+92 300 1234567",
        "store_email": settings.contact_email or "care@aanganliving.pk",
        "store_logo": settings.logo.url if settings.logo else "",
        "store_favicon": settings.favicon.url if settings.favicon else "",
        "theme_primary": settings.primary_color or "#3F3A33",
        "theme_secondary": settings.secondary_color or "#B4684A",
        "announcement": (
            settings.announcement_text if settings.announcement_active else ""
        ),
        "social_links": {
            "facebook": settings.facebook_url,
            "instagram": settings.instagram_url,
            "pinterest": settings.pinterest_url,
            "youtube": settings.youtube_url,
        },
        **_cart_data(request),
        **_wishlist_data(request),
    }
