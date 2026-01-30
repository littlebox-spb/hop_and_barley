from typing import TYPE_CHECKING

from django.contrib.auth.models import AbstractUser
from django.db import models


if TYPE_CHECKING:
    import datetime


class User(AbstractUser):
    phone: str | None = models.CharField(
        max_length=20, blank=True, null=True, verbose_name="Телефон"
    )  # type: ignore[assignment]
    created_at: "datetime.datetime" = models.DateTimeField(auto_now_add=True)  # type: ignore[assignment]
    updated_at: "datetime.datetime" = models.DateTimeField(auto_now=True)  # type: ignore[assignment]

    def __str__(self: "User") -> str:
        return self.username
