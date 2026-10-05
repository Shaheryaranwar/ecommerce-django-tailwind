from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_POST

from products.models import ProductVariant

from .models import Cart, CartItem


def _get_cart(request):
    cart_id = request.session.get("cart_id")
    if cart_id:
        cart, created = Cart.objects.get_or_create(id=cart_id)
    else:
        cart = Cart.objects.create()
        request.session["cart_id"] = cart.id
    return cart


def _cart_payload(cart):
    return {
        "count": cart.item_count,
        "subtotal": float(cart.get_total_cost()),
        "free_delivery_threshold": float(settings.FREE_DELIVERY_THRESHOLD),
    }


def _json_response(cart, **extra):
    return JsonResponse({**_cart_payload(cart), **extra})


@require_POST
def cart_add(request, variant_id):
    cart = _get_cart(request)
    variant = get_object_or_404(
        ProductVariant.objects.select_related("product"),
        id=variant_id,
        is_active=True,
    )
    quantity = int(request.POST.get("quantity", 1) or 1)
    quantity = max(1, min(quantity, 20))

    if variant.stock <= 0:
        return JsonResponse(
            {"success": False, "message": "This item is currently out of stock."},
            status=400,
        )

    item, created = CartItem.objects.get_or_create(cart=cart, variant=variant)
    if not created:
        item.quantity += quantity
    else:
        item.quantity = quantity
    item.quantity = min(item.quantity, max(variant.stock, item.quantity))
    item.save()

    return _json_response(
        cart,
        success=True,
        message=f"{variant.product.name} added to your cart.",
        item_id=item.id,
        quantity=item.quantity,
    )


@require_POST
def cart_update(request, item_id):
    cart = _get_cart(request)
    item = get_object_or_404(CartItem, id=item_id, cart=cart)
    quantity = int(request.POST.get("quantity", 1) or 1)
    quantity = max(1, min(quantity, 20))
    item.quantity = quantity
    item.save()
    return _json_response(
        cart,
        success=True,
        quantity=item.quantity,
        item_total=float(item.get_total_price()),
        item_id=item.id,
    )


@require_POST
def cart_remove(request, item_id):
    cart = _get_cart(request)
    item = get_object_or_404(CartItem, id=item_id, cart=cart)
    item.delete()
    return _json_response(cart, success=True, message="Item removed from your cart.")


def cart_detail(request):
    cart_id = request.session.get("cart_id")
    cart = Cart.objects.filter(id=cart_id).prefetch_related(
        "items__variant__product__images"
    ).first()
    context = {
        "cart": cart,
        "free_delivery_threshold": settings.FREE_DELIVERY_THRESHOLD,
        "delivery_fee": settings.DELIVERY_FEE,
    }
    return render(request, "cart/cart.html", context)
