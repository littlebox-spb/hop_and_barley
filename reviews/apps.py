"""Модуль приложения для модели отзывов."""

from django.apps import AppConfig


class ReviewsConfig(AppConfig):
    """Класс приложения для модели отзывов."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "reviews"
