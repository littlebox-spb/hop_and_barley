"""Admin panel for orders."""

from typing import TYPE_CHECKING, Any

from django.contrib import admin
from django.db.models import Sum
from django.http import HttpRequest, HttpResponse

from .models import Order, OrderItem

if TYPE_CHECKING:
    OrderItemTab = admin.TabularInline[OrderItem, Any]
    OrderModel = admin.ModelAdmin[Order]
else:
    OrderItemTab = admin.TabularInline
    OrderModel = admin.ModelAdmin


class OrderItemInline(OrderItemTab):
    """Inline for order items."""

    model = OrderItem
    extra = 0
    readonly_fields = ["price"]


@admin.register(Order)
class OrderAdmin(OrderModel):
    """Admin panel for orders."""

    list_display = ("id", "user", "total_price", "created_at", "is_paid")
    list_filter = ("is_paid", "created_at")
    inlines = [OrderItemInline]

    def changelist_view(
        self, request: HttpRequest, extra_context: dict[str, Any] | None = None
    ) -> HttpResponse:
        """Add total revenue to the changelist view."""
        aggregate_data = Order.objects.aggregate(total=Sum("total_price"))
        extra_context = extra_context or {}
        extra_context["total_revenue"] = aggregate_data["total"]
        return super().changelist_view(request, extra_context=extra_context)
