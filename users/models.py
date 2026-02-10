"""Models for the users app."""

from typing import TYPE_CHECKING

from django.contrib.auth.models import AbstractUser
from django.db import models

if TYPE_CHECKING:
    from datetime import datetime


class User(AbstractUser):
    """Custom user model with additional fields."""

    phone: str = models.CharField(
        max_length=20, blank=True, default="", verbose_name="Телефон"
    )  # type: ignore[assignment]
    created_at: "datetime" = models.DateTimeField(auto_now_add=True)  # type: ignore[assignment]
    updated_at: "datetime" = models.DateTimeField(auto_now=True)  # type: ignore[assignment]

    def __str__(self: "User") -> str:
        """Return the username of the user."""
        return self.username
