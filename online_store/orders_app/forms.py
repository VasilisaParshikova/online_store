from django.forms import ModelForm
from orders_app.models import Order


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ["user", "delivery", "cost", "payment_type", "city", "address"]
