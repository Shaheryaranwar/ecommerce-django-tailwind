from django.shortcuts import render, redirect, get_object_or_404
from orders.models import Order
from .models import Payment
from .services import cod, stripe, paypal, jazzcash, easypaisa

SERVICE_MAP = {
    "cod": cod.process_cod,
    "stripe": stripe.process_stripe,
    "paypal": paypal.process_paypal,
    "jazzcash": jazzcash.process_jazzcash,
    "easypaisa": easypaisa.process_easypaisa,
}

def select_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, "payments/select_method.html", {"order": order})

def process_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    # ✅ PREVENT DUPLICATE PAYMENTS
    if hasattr(order, "payment"):
        return redirect("payments:success", order.payment.id)

    if request.method == "POST":
        method = request.POST.get("method")

        if not method:
            return render(request, "payments/process.html", {
                "order": order,
                "error": "Please select a payment method."
            })

        # ✅ CREATE PAYMENT FIRST (VERY IMPORTANT)
        payment = Payment.objects.create(
            order=order,
            method=method,
            amount=order.get_total_cost(),
            status="pending",
        )

        # 🔹 CASH ON DELIVERY
        if method == "cod":
            payment.status = "pending"
            payment.transaction_id = "COD"
            payment.save()
            return redirect("payments:success", payment.id)

        # 🔹 STRIPE
        elif method == "stripe":
            return redirect("payments:stripe_start", payment.id)

        # 🔹 PAYPAL
        elif method == "paypal":
            return redirect("payments:paypal_start", payment.id)

        # 🔹 JAZZCASH
        elif method == "jazzcash":
            payment.transaction_id = "JAZZCASH-MANUAL"
            payment.save()
            return redirect("payments:success", payment.id)

        # 🔹 EASYPAISA
        elif method == "easypaisa":
            payment.transaction_id = "EASYPAISA-MANUAL"
            payment.save()
            return redirect("payments:success", payment.id)

    return render(request, "payments/process.html", {"order": order})

def payment_success(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)
    return render(request, "payments/success_method.html", {"payment": payment})

def payment_failed(request):
    return render(request, "payments/failed.html")
