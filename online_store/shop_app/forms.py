from django.forms import ModelForm
from shop_app.models import Review


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = "__all__"

