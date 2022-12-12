from django.contrib.auth.models import User
from colorfield.fields import ColorField
from users.models import CustomUser
from .models import Review, Category, Product, Image
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name"]


class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)

    class Meta:
        model = Review
        fields = ['id', 'user', 'text', 'stars', 'time_create']
        read_only_fields = ['time_create']


class ReviewCreateSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=200, required=True)
    stars = serializers.IntegerField(min_value=1, max_value=5, required=True)

    def create(self, validated_data):
        return Review.objects.create(**validated_data)


class CategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=255)

    class Meta:
        model = Category
        fields = ["id", "name"]


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ["id", "image"]


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id", "name", "price", "get_color", "get_image", "size"
        ]


class ProductDetailSerializer(serializers.ModelSerializer):
    image = ImageSerializer(many=True)

    class Meta:
        model = Product
        fields = [
            "id", "name", "price",
            "image", "color", "size",
            "description", "details_and_care"
        ]
