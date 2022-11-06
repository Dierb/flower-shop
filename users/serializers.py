from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import EmailAddress, CustomUser


class UserCreateSerializer(serializers.Serializer):
    nickname = serializers.CharField()
    password = serializers.CharField(min_length=8)
    email = serializers.EmailField()
    phone_number = serializers.CharField(min_length=12)

    def validate_nickname(self, nickname):
        if CustomUser.objects.filter(nickname=nickname):
            raise ValidationError('This nickname is already taken')
        return nickname

    def validate_email(self, email):
        if EmailAddress.objects.filter(email=email):
            raise ValidationError('Email already registered')
        return email


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = 'id nickname first_name last_name is_active'.split()


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(
        max_length=100,
        style={'placeholder': 'email', 'autofocus': True}
    )
    password = serializers.CharField(
        max_length=100,
        style={'input_type': 'password', 'placeholder': 'Password'}
    )
    remember_me = serializers.BooleanField(required=False, default=False)

