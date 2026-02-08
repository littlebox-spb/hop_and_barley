from typing import TYPE_CHECKING

from django import forms

from products.models import Product

if TYPE_CHECKING:
    ProductAdmin = forms.ModelForm[Product]
else:
    ProductAdmin = forms.ModelForm


class ProductAdminForm(ProductAdmin):
    class Meta:
        model = Product
        fields = [
            "name",
            "description",
            "price",
            "stock",
            "category",
            "is_active",
        ]
