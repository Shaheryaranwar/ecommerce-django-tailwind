from django.shortcuts import render, get_object_or_404
from products.models import Product
from .models import Cart, CartItem
from django.views.decorators.http import require_POST
from django.http import JsonResponse


def _get_cart(request):
    cart_id = request.session.get("cart_id")
    if cart_id:
        cart, _ = Cart.objects.get_or_create(id=cart_id)
    else:
        cart = Cart.objects.create()
        request.session["cart_id"] = cart.id
    return cart


@require_POST
def cart_add(request, product_id):
    cart = _get_cart(request)
    product = get_object_or_404(Product, id=product_id, is_active=True)

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart, product=product
    )
    if not created:
        cart_item.quantity += 1
    cart_item.save()

    return JsonResponse({
        "success": True,
        "quantity": cart_item.quantity,
        "item_total": cart_item.get_total_price(),
        "cart_total": cart.get_total_cost(),
    })


@require_POST
def cart_decrease(request, product_id):
    cart = _get_cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart_item = get_object_or_404(CartItem, cart=cart, product=product)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    return JsonResponse({
        "success": True,
        "quantity": cart_item.quantity if cart_item.id else 0,
        "item_total": cart_item.get_total_price() if cart_item.id else 0,
        "cart_total": cart.get_total_cost(),
    })


def cart_detail(request):
    cart_id = request.session.get("cart_id")
    cart = Cart.objects.filter(id=cart_id).first()
    return render(request, "carts/cart_detail.html", {"cart": cart})
