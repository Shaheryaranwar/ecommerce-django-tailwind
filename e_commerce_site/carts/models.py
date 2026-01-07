from django.db import models
from products.models import Product
# Create your models here.
class Cart(models.Model):
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def get_total_cost(self):
        total=sum(item.get_total_price() for item in self.items.all())
        return total


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='cart_items', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def get_total_price(self):
        variant = self.product.variants.first()
        if variant:
            return variant.price * self.quantity
        return 0