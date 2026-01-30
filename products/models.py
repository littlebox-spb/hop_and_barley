from typing import Any, Self

from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name: str = models.CharField(max_length=200)  # type: ignore[assignment]
    slug: str = models.SlugField(unique=True)  # type: ignore[assignment]
    parent: Self | None = models.ForeignKey(
        "self", blank=True, null=True, related_name="children", on_delete=models.CASCADE
    )  # type: ignore[assignment]

    def save(self: Self, *args: Any, **kwargs: Any) -> None:
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    name: str = models.CharField(max_length=200)  # type: ignore[assignment]
    slug: str = models.SlugField(unique=True)  # type: ignore[assignment]
    category: Category = models.ForeignKey(Category, on_delete=models.CASCADE)  # type: ignore[assignment]
    description: str = models.TextField()  # type: ignore[assignment]
    price: float = models.DecimalField(max_digits=10, decimal_places=2)  # type: ignore[assignment]
    stock: int = models.PositiveIntegerField(default=0)  # type: ignore[assignment]
    is_active: bool = models.BooleanField(default=True)  # type: ignore[assignment]

    def save(self: Self, *args: Any, **kwargs: Any) -> None:
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name
