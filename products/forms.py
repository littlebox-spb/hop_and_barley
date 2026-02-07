from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            "name",
            "description",
            "price",
            "category",
            "is_active",
            "picture_url",
        ]

        widgets = {
            "name": forms.TextInput(attrs={"class": "Input", "style": "height: 48px;"}),
            "description": forms.Textarea(
                attrs={"class": "Textarea", "rows": 5, "style": "min-height: 120px;"}
            ),
            "price": forms.NumberInput(
                attrs={"class": "Input", "style": "height: 48px;"}
            ),
            "category": forms.Select(
                attrs={"class": "Input", "style": "height: 48px;"}
            ),
        }
