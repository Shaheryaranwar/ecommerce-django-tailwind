from django import forms

from .models import Order


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            "first_name",
            "last_name",
            "email",
            "phone",
            "address",
            "city",
            "country",
            "postal_code",
            "notes",
        ]
        widgets = {
            "first_name": forms.TextInput(attrs={"placeholder": "First name"}),
            "last_name": forms.TextInput(attrs={"placeholder": "Last name"}),
            "email": forms.EmailInput(attrs={"placeholder": "you@example.com"}),
            "phone": forms.TextInput(attrs={"placeholder": "03XX XXXXXXX"}),
            "address": forms.TextInput(attrs={"placeholder": "House, street, area"}),
            "city": forms.TextInput(attrs={"placeholder": "City"}),
            "country": forms.TextInput(attrs={"placeholder": "Pakistan"}),
            "postal_code": forms.TextInput(attrs={"placeholder": "Postal code (optional)"}),
            "notes": forms.Textarea(
                attrs={"rows": 3, "placeholder": "Delivery notes (optional)"}
            ),
        }
