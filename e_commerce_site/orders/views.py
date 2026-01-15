from django.shortcuts import render, get_object_or_404, redirect
from carts.models import Cart
from .forms import OrderCreateForm
from .models import OrderItem, Order


def order_created(request):
    cart = None
    cart_id = request.session.get("cart_id")

    if cart_id:
        cart = Cart.objects.filter(id=cart_id).first()

    # If cart is empty, redirect
    if not cart or not cart.items.exists():
        return redirect("carts:cart_detail")

    if request.method == "POST":
        form = OrderCreateForm(request.POST)

        if form.is_valid():
            order = form.save(commit=False)
            order.save()

            # Create OrderItems
            for item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    price=item.product.variants.first().price if item.product.variants.exists() else 0,
                    quantity=item.quantity,
                )

            # Clear cart AFTER loop
            cart.delete()
            del request.session["cart_id"]

            return redirect("orders:order_confirmation", order_id=order.id)

    else:
        form = OrderCreateForm()

    return render(
        request,
        "orders/order_created.html",
        {"cart": cart, "form": form},
    )


def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(
        request,
        "orders/order_confirmation.html",
        {"order": order},
    )
