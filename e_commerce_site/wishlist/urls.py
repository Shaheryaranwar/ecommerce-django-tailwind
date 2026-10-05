from django.urls import path

from . import views

app_name = "wishlist"

urlpatterns = [
    path("", views.wishlist_page, name="wishlist"),
    path("toggle/<int:product_id>/", views.wishlist_toggle, name="toggle"),
]
