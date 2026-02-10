"""Forms for the products app."""

from typing import TYPE_CHECKING

from django import forms

from .models import Product

if TYPE_CHECKING:
    FormProduct = forms.ModelForm[Product]
else:
    FormProduct = forms.ModelForm


class ProductForm(FormProduct):
    """Product form."""

    class Meta:
        """Meta class for the form."""

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
