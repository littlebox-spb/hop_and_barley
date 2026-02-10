"""Модуль приложения для управления пользователями."""

from django.apps import AppConfig


class UsersConfig(AppConfig):
    """Класс конфигурации приложения."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "users"
