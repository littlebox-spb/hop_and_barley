from django.contrib.auth.views import LoginView, LogoutView
from django.urls import URLPattern, path

from .views import ProfileView, RegisterView, logout_view

urlpatterns: list[URLPattern] = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", logout_view, name="logout"),
    path(
        "fogot/",
        LoginView.as_view(template_name="forgot_password.html"),
        name="password_reset",
    ),
    path("profile/", ProfileView.as_view(), name="profile"),
]
