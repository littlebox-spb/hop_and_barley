from typing import TYPE_CHECKING

from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import RegisterForm

if TYPE_CHECKING:
    from .models import User

    ViewRegister = CreateView[User, RegisterForm]
else:
    ViewRegister = CreateView


class RegisterView(ViewRegister):
    form_class = RegisterForm
    template_name = "register.html"
    success_url = reverse_lazy("login")
