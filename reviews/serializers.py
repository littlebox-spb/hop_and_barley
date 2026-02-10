"""Serializers for reviews."""

from typing import Any

from rest_framework import serializers

from .models import Review


class ReviewSerializer(serializers.ModelSerializer[Review]):
    """Serializer for reviews."""

    user: Any = serializers.StringRelatedField()

    class Meta:
        """Meta class for the serializer."""

        model = Review
        fields = [
            "id",
            "user",
            "rating",
            "text",
            "created_at",
        ]
