from typing import TYPE_CHECKING

from django.conf import settings
from django.db import models

from products.models import Product

if TYPE_CHECKING:
    from datetime import datetime

    from users.models import User


class Order(models.Model):
    user: "User" = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders"
    )  # type: ignore[assignment]
    created: "datetime" = models.DateTimeField(auto_now_add=True)  # type: ignore[assignment]
    is_paid: bool = models.BooleanField(default=False)  # type: ignore[assignment]

    def __str__(self) -> str:
        return f"Order {self.id}"


class OrderItem(models.Model):
    order: Order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="items"
    )  # type: ignore[assignment]
    product: Product = models.ForeignKey(Product, on_delete=models.CASCADE)  # type: ignore[assignment]
    quantity: int = models.PositiveIntegerField(default=1)  # type: ignore[assignment]
    price: float = models.DecimalField(max_digits=10, decimal_places=2)  # type: ignore[assignment]

    def __str__(self) -> str:
        return f"{self.product} x {self.quantity}"
