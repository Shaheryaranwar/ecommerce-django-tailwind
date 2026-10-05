import secrets

from .models import Payment


def create_payment(order, method):
    """Create a payment record for the order using the chosen method."""
    return Payment.objects.create(order=order, method=method, amount=order.get_total_cost())


def process(payment):
    """Simulate gateway processing.

    COD stays pending (cash collected on delivery); card / wallet methods
    succeed immediately in development. Swap for real gateways in production.
    """
    if payment.method == "cod":
        payment.status = "pending"
        payment.transaction_id = f"COD-{payment.order.id}"
    else:
        payment.status = "success"
        payment.transaction_id = f"{payment.method.upper()}-{secrets.token_hex(6).upper()}"

    payment.save()

    if payment.status == "success":
        payment.order.paid = True
        payment.order.save(update_fields=["paid"])

    return payment
