"""Serializers for tracker app"""

from rest_framework.serializers import ModelSerializer, CharField, ValidationError
from .models import Category, TOTAL_USER_CATEGORIES


class CategorySerializer(ModelSerializer):
    """Serializer for Category Model"""
    user = CharField(source="user.username", read_only=True)

    class Meta:
        model = Category
        fields = "id", "name", "user"
        read_only = "id",

    def create(self, validated_data: dict):
        """Override creat method to check total number of Categories created by current user"""
        # Check if User has already max. number of categories and raise Validation Error
        if Category.objects.filter(user_id=validated_data["user_id"]).count() >= \
                TOTAL_USER_CATEGORIES:
            raise ValidationError(f"Cannot create more than {TOTAL_USER_CATEGORIES} categories.")
        return super(CategorySerializer, self).create(validated_data)
