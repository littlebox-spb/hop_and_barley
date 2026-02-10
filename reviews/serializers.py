from rest_framework import serializers
from .models import Review


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Review
        fields = [
            "id",
            "user",
            "rating",
            "text",
            "created_at",
        ]
