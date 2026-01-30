from typing import TYPE_CHECKING

from django.conf import settings
from django.db import models

from products.models import Product

if TYPE_CHECKING:
    from datetime import datetime

from users.models import User


class Review(models.Model):
    product: Product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="reviews"
    )  # type: ignore[assignment]
    user: User = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # type: ignore[assignment]
    rating: int = models.PositiveIntegerField()  # type: ignore[assignment]
    text: str = models.TextField()  # type: ignore[assignment]
    created_at: "datetime" = models.DateTimeField(auto_now_add=True)  # type: ignore[assignment]

    def __str__(self) -> str:
        return f"Review {self.rating}/5"
