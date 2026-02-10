"""Admin panel for the products app."""

from typing import TYPE_CHECKING

from django.contrib import admin

from products.models import Category, Product

if TYPE_CHECKING:
    ModelAdminCategory = admin.ModelAdmin[Category]
    ModelAdminProduct = admin.ModelAdmin[Product]
else:
    ModelAdminCategory = admin.ModelAdmin
    ModelAdminProduct = admin.ModelAdmin


@admin.register(Category)
class CategoryAdmin(ModelAdminCategory):
    """Admin panel for categories."""

    list_display = ["name", "parent"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Product)
class ProductAdmin(ModelAdminProduct):
    """Admin panel for products."""

    list_display = ["name", "category", "price", "stock", "is_active"]
    list_filter = ["category", "is_active"]
    prepopulated_fields = {"slug": ("name",)}
