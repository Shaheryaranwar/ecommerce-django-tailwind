from django.urls import path
from . import views

app_name = "payments"

urlpatterns = [
    path("select/<int:order_id>/", views.select_payment, name="select"),
    path("process/<int:order_id>/", views.process_payment, name="process"),
    path("success/<int:payment_id>/", views.payment_success, name="success"),
    path("failed/", views.payment_failed, name="failed"),
]
