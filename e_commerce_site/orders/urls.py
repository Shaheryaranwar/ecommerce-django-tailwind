from django.urls import path
from .views import  order_created, order_confirmation

app_name = "orders"
urlpatterns = [
    path("create/", order_created, name="order_created"),
    path("confirmation/<int:order_id>/", order_confirmation, name="order_confirmation"),
]