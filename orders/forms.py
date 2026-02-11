"""Forms for the orders app."""

from typing import TYPE_CHECKING

from django import forms

from .models import Order

if TYPE_CHECKING:
    OrderForm = forms.ModelForm[Order]
else:
    OrderForm = forms.ModelForm


class OrderCreateForm(OrderForm):
    """Form for creating an order."""

    address = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 3, "class": "Textarea"})
    )
    city = forms.CharField(widget=forms.TextInput(attrs={"class": "Input"}))
    phone = forms.CharField(widget=forms.TextInput(attrs={"class": "Input"}))
    full_name = forms.CharField(widget=forms.TextInput(attrs={"class": "Input"}))

    class Meta:
        """Meta class for the form."""

        model = Order
        fields = ["full_name", "phone", "city", "address"]
