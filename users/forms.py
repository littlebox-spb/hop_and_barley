"""Forms for the users app."""

from typing import TYPE_CHECKING

from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User

if TYPE_CHECKING:
    UserCreation = UserCreationForm[User]
else:
    UserCreation = UserCreationForm


class RegisterForm(UserCreation):
    """Register form."""

    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=12, required=True)

    class Meta:
        """Meta class for the form."""

        model = User
        fields = ("username", "email", "phone", "password1", "password2")
