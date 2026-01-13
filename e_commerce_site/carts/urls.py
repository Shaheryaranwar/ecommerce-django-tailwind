from django.urls import path
from .views import cart_detail, cart_add, cart_decrease

app_name = "carts"

urlpatterns = [
    path("", cart_detail, name="cart_detail"),
    path("add/<int:product_id>/", cart_add, name="cart_add"),
    path("decrease/<int:product_id>/", cart_decrease, name="cart_decrease"),
]
