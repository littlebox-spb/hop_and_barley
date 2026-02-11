"""Модуль приложения для модели заказов."""

from django.apps import AppConfig


class OrdersConfig(AppConfig):
    """Класс приложения для модели заказов."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "orders"
