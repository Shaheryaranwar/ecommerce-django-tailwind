import django.forms as forms
from .models import Order
class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address', 'city']
        error_messages = {
            'first_name': {'required': ''},
            'last_name': {'required': ''},
            'email': {'required': ''},
            'address': {'required': ''},
            'city': {'required': ''},
        }