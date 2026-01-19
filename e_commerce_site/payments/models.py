from django.db import models
from orders.models import Order

class Payment(models.Model):
    PAYMENT_METHODS = [
        ("cod", "Cash on Delivery"),
        ("stripe", "Stripe"),
        ("paypal", "PayPal"),
        ("jazzcash", "JazzCash"),
        ("easypaisa", "EasyPaisa"),
    ]

    PAYMENT_STATUS = [
        ("pending", "Pending"),
        ("success", "Success"),
        ("failed", "Failed"),
    ]

    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="payment")
    method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default="pending")
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    
    transaction_id = models.CharField(max_length=100, blank=True, null=True)


    def __str__(self):
        return f"{self.order.id} - {self.method}"
