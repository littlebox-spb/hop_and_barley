from django.contrib.auth.views import LoginView, LogoutView
from django.urls import URLPattern, path

from .views import RegisterView

urlpatterns: list[URLPattern] = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", LogoutView.as_view(next_page="home"), name="logout"),
    path(
        "fogot/",
        LoginView.as_view(template_name="forgot_password.html"),
        name="password_reset",
    ),
]
