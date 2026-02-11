"""Serializers for orders."""

from rest_framework import serializers

from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer[OrderItem]):
    """Serializer for order items."""

    class Meta:
        """Meta class for the serializer."""

        model = OrderItem
        fields = ["id", "product", "quantity", "price"]


class OrderSerializer(serializers.ModelSerializer[Order]):
    """Serializer for orders."""

    items = OrderItemSerializer(many=True, read_only=True)
    user = serializers.ReadOnlyField(source="user.username")

    class Meta:
        """Meta class for the serializer."""

        model = Order
        fields = [
            "id",
            "user",
            "full_name",
            "phone",
            "city",
            "address",
            "total_price",
            "items",
            "created_at",
        ]
