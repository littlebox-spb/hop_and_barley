from typing import TYPE_CHECKING

from django.contrib import admin

from .models import Order, OrderItem

if TYPE_CHECKING:
    TabularInlineItem = admin.TabularInline[OrderItem, Order]
    ModelAdminOrder = admin.ModelAdmin[Order]
else:
    TabularInlineItem = admin.TabularInline
    ModelAdminOrder = admin.ModelAdmin


class OrderItemInline(TabularInlineItem):
    model = OrderItem
    extra = 1


@admin.register(Order)
class OrderAdmin(ModelAdminOrder):
    inlines = [OrderItemInline]
    list_display = ["id", "user", "created", "is_paid"]
