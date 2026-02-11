"""Модуль заказов."""

from django.conf import settings
from django.db import models

from products.models import Product

STATUS_CHOICES = [
    ("pending", "Pending"),
    ("paid", "Paid"),
    ("shipped", "Shipped"),
    ("delivered", "Delivered"),
    ("cancelled", "Cancelled"),
]

User = settings.AUTH_USER_MODEL


class Order(models.Model):
    """Модель заказа."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    full_name = models.CharField(max_length=100, default="")
    phone = models.CharField(max_length=20, default="")
    city = models.CharField(max_length=100, default="")
    address = models.TextField(default="")
    created_at = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)

    class Meta:
        """Метаданные модели заказа."""

        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self) -> str:
        """Возвращает строковое представление заказа."""
        return f"Order #{self.id} by {self.user}"


class OrderItem(models.Model):
    """Модель товара в заказе."""

    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self) -> str:
        """Возвращает строковое представление товара в заказе."""
        return f"{self.product.name} x {self.quantity}"
