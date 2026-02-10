"""Views for the users app."""

from typing import TYPE_CHECKING, Any, Self, cast

from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, TemplateView

from orders.models import Order

from .forms import RegisterForm
from .models import User

if TYPE_CHECKING:
    ViewRegister = CreateView[User, RegisterForm]
else:
    ViewRegister = CreateView


class RegisterView(ViewRegister):
    """Register view."""

    form_class = RegisterForm
    template_name = "register.html"
    success_url = reverse_lazy("login")


class ProfileView(LoginRequiredMixin, TemplateView):
    """Profile view."""

    template_name = "account.html"

    def get_context_data(self: Self, **kwargs: Any) -> dict[str, Any]:
        """Get context data."""
        user = cast(User, self.request.user)
        context = super().get_context_data(**kwargs)
        context["orders"] = Order.objects.filter(user=user).order_by("-created_at")
        return context


@require_POST
def logout_view(request: Any) -> Any:
    """Logout view."""
    logout(request)
    return redirect("home")
