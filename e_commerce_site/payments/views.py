from django.shortcuts import render, get_object_or_404, redirect
from orders.models import Order
from .models import Payment

def payment_select(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.method == "POST":
        method = request.POST.get("payment_method")

        # Decide currency
        currency = "USD" if method in ['stripe', 'paypal'] else "PKR"

        payment = Payment.objects.create(
            order=order,
            method=method,
            amount=order.get_total_cost(),
            currency=currency,
            status='pending'
        )

        # ROUTING BASED ON METHOD
        if method == 'cod':
            payment.status = 'success'
            payment.save()
            order.paid = True
            order.save()
            return redirect("payments:success", order.id)

        if method == 'bank':
            return redirect("payments:bank_instructions", payment.id)

        if method in ['stripe', 'paypal']:
            return redirect("payments:international_process", payment.id)

        if method in ['jazzcash', 'easypaisa']:
            return redirect("payments:pakistan_process", payment.id)

    return render(request, "payments/select.html", {"order": order})
def payment_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, "payments/success.html", {"order": order})

def pakistan_process(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)

    # Simulate payment success (for now)
    payment.status = 'success'
    payment.transaction_id = f"PK-{payment.id}"
    payment.gateway_response = {"message": "Payment successful"}
    payment.save()

    order = payment.order
    order.paid = True
    order.save()

    return redirect("payments:success", order.id)

def international_process(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)

    # Placeholder (Stripe/PayPal will go here)
    payment.status = 'processing'
    payment.save()

    return render(request, "payments/international_processing.html", {
        "payment": payment
    })

def bank_instructions(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)
    return render(request, "payments/bank_instructions.html", {
        "payment": payment
    })

def success(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, "payments/success.html", {"order": order})

