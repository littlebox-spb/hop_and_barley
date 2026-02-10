"""Serializers for products."""

from rest_framework import serializers

from reviews.models import Review

from .models import Category, Product


class CategorySerializer(serializers.ModelSerializer[Category]):
    """Serializer for categories."""

    class Meta:
        """Meta class."""

        model = Category
        fields = "__all__"


class ReviewSerializer(serializers.ModelSerializer[Review]):
    """Serializer for reviews."""

    user = serializers.ReadOnlyField(source="user.username")

    class Meta:
        """Meta class."""

        model = Review
        fields = ["id", "user", "rating", "text", "created_at"]


class ProductSerializer(serializers.ModelSerializer[Product]):
    """Serializer for products."""

    category = CategorySerializer(read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        """Meta class for the serializer."""

        model = Product
        fields = [
            "id",
            "name",
            "slug",
            "category",
            "description",
            "price",
            "stock",
            "reviews",
            "picture_url",
        ]
