import django.forms as forms
from .models import Order
class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'phone', 'email', 'address', 'city']
        error_messages = {
            'first_name': {'required': ''},
            'last_name': {'required': ''},
            'phone': {'required': ''},
            'email': {'required': ''},
            'address': {'required': ''},
            'city': {'required': ''},
        }