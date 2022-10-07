from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError

from .models import EmailAddress


class UserCreateSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(min_length=8)
    email = serializers.EmailField()

    def validate_username(self, username):
        if User.objects.filter(username=username):
            raise ValidationError('User already exists')
        return username

    def validate_email(self, email):
        if EmailAddress.objects.filter(email=email):
            raise ValidationError('Email already registered')
        return email


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = 'id username first_name last_name is_active'.split()
