from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from cart.models import Cart
from payments.services import create_payment, process

from .forms import OrderCreateForm
from .models import Order, OrderItem

PAYMENT_METHODS = [
    ("cod", "Cash on Delivery", "Pay in cash when your order arrives at your doorstep."),
    ("card", "Debit / Credit Card", "Pay securely online with Visa, Mastercard or UnionPay."),
    ("jazzcash", "JazzCash", "Pay instantly with your JazzCash mobile wallet."),
    ("easypaisa", "EasyPaisa", "Pay instantly with your EasyPaisa mobile wallet."),
]


def _active_cart(request):
    cart_id = request.session.get("cart_id")
    if not cart_id:
        return None
    return Cart.objects.filter(id=cart_id).prefetch_related(
        "items__variant__product__images"
    ).first()


def checkout(request):
    cart = _active_cart(request)
    if not cart or not cart.items.exists():
        return redirect("cart:cart_detail")

    initial = {}
    if request.user.is_authenticated:
        profile = getattr(request.user, "profile", None)
        if profile:
            initial.update(
                {
                    "first_name": request.user.first_name,
                    "last_name": request.user.last_name,
                    "email": request.user.email,
                    "phone": profile.phone,
                    "address": profile.address,
                    "city": profile.city,
                    "country": profile.country,
                    "postal_code": profile.postal_code,
                }
            )

    form = OrderCreateForm(request.POST or None, initial=initial)

    if request.method == "POST" and form.is_valid():
        method = request.POST.get("payment_method", "cod")
        if method not in {m[0] for m in PAYMENT_METHODS}:
            method = "cod"

        order = form.save(commit=False)
        order.user = request.user if request.user.is_authenticated else None
        order.status = "confirmed"
        order.save()

        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.variant.product,
                variant_name=item.variant.name,
                sku=item.variant.sku,
                price=item.variant.price,
                quantity=item.quantity,
            )

        payment = create_payment(order, method)
        process(payment)

        cart.delete()
        request.session.pop("cart_id", None)
        request.session["last_order_id"] = order.id
        messages.success(request, f"Order #{order.id} placed successfully.")

        return redirect("orders:order_success", order_id=order.id)

    subtotal = cart.get_total_cost()
    delivery_fee = 0 if subtotal >= settings.FREE_DELIVERY_THRESHOLD else settings.DELIVERY_FEE

    return render(
        request,
        "orders/checkout.html",
        {
            "cart": cart,
            "form": form,
            "payment_methods": PAYMENT_METHODS,
            "subtotal": subtotal,
            "delivery_fee": delivery_fee,
            "total": subtotal + delivery_fee,
            "free_delivery_threshold": settings.FREE_DELIVERY_THRESHOLD,
        },
    )


def _can_view_order(request, order):
    if request.session.get("last_order_id") == order.id:
        return True
    return request.user.is_authenticated and order.user_id == request.user.id


def order_success(request, order_id):
    order = get_object_or_404(
        Order.objects.prefetch_related("items__product__images").select_related("payment"),
        id=order_id,
    )
    if not _can_view_order(request, order):
        return redirect("core:home")
    return render(request, "orders/order_success.html", {"order": order})


@login_required
def order_history(request):
    orders = (
        Order.objects.filter(user=request.user)
        .prefetch_related("items__product__images")
        .select_related("payment")
    )
    return render(request, "orders/order_history.html", {"orders": orders})


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(
        Order.objects.prefetch_related("items__product__images").select_related("payment"),
        id=order_id,
        user=request.user,
    )
    return render(request, "orders/order_detail.html", {"order": order})
