from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import EmailAddress, CustomUser
from .token import account_activation_token


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

    def validate_email(self, email):
        if not CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError('User with specified email is not registered')
        return email

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        user = CustomUser.objects.get(email=email)
        if not user.check_password(password):
            raise serializers.ValidationError('Wrong password!!!')
        return super().validate(attrs)


class RestorePasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, email):
        if CustomUser.objects.get(email=email) is None:
            raise serializers.ValidationError("User with this email does not exists")
        else:
            return email

    def send_password_change_form(self):
        email = self.validated_data.get('email')
        user = CustomUser.objects.get(email=email)
        current_site = get_current_site(self.context['request'])
        message = render_to_string('users/restore_account.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        mail_subject = 'Please click on the link to restore your account,'
        to_email = self.validated_data.get('email')
        email = EmailMessage(
            mail_subject, message, to=[to_email]
        )
        email.send()


class RestorePasswordCompleteSerialaizer(serializers.Serializer):
    password = serializers.CharField(min_length=8)
    password_confirm = serializers.CharField(min_length=8)

    def validate(self, attrs):
        pass1 = attrs.get('password')
        pass2 = attrs.get('password_confirm')
        if pass1 != pass2:
            raise serializers.ValidationError("Passwords don't match")
        if len(pass2) < 8:
            raise serializers.ValidationError('password length must be greater than or equal to 8')

        return super().validate(attrs)


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(min_length=8)
    password = serializers.CharField(min_length=8)
    password_confirm = serializers.CharField(min_length=8)

    def validate_old_password(self, password):
        user = self.context['request'].user
        if not user.check_password(password):
            raise serializers.ValidationError('Wrong password')
        return password

    def validate(self, attrs):
        pass1 = attrs.get('password')
        pass2 = attrs.get('password_confirm')
        if pass1 != pass2:
            raise serializers.ValidationError("Passwords don't match")
        return super().validate(attrs)

    def set_new_password(self):
        user = self.context['request'].user
        password = self.validated_data.get('password')
        user.set_password(password)
        user.save()
