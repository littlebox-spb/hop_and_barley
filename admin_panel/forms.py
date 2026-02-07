# admin_panel/forms.py
from django import forms
from products.models import Product


class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            "name",
            "description",
            "price",
            "category",
            "is_active",
        ]
