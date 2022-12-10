import os
import random

from django.contrib.auth import get_user_model, authenticate
from rest_framework import authentication
from rest_framework import exceptions
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed

from .models import CustomUser


class CustomAuthentication(TokenAuthentication):
    def authenticate_credentials(self, key):
        model = self.get_model()
        try:
            token = model.objects.select_related('user').get(key=key)
        except model.DoesNotExist:
            raise exceptions.AuthenticationFailed(('Invalid token.'))

        if not token.user.is_active:
            raise exceptions.AuthenticationFailed(('User inactive or deleted.'))

        return (token.user, token)


def generate_nickname(nickname):

    nickname = "".join(nickname.split(' ')).lower()
    if not CustomUser.objects.filter(nickname=nickname).exists():
        return nickname
    else:
        random_nickname = nickname + str(random.randint(0, 1000))
        return generate_nickname(random_nickname)


def register_social_user(provider, user_id, email, name):
    filtered_user_by_email = CustomUser.objects.filter(email=email)
    print(f"email {email}, name {name}, provider {provider}")

    if filtered_user_by_email.exists():

        if provider == filtered_user_by_email[0].auth_provider:

            registered_user = authenticate(
                email=email, password=os.environ.get('SOCIAL_SECRET'))

            try:
                token = Token.objects.get(user=registered_user)
            except Token.DoesNotExist:
                token = Token.objects.create(user=registered_user)

            return {
                'nickname': registered_user.nickname,
                'email': registered_user.email,
                'token': token.key}

        else:
            raise AuthenticationFailed(
                detail='Please continue your login using ' + filtered_user_by_email[0].auth_provider)

    else:
        user = {
            'nickname': generate_nickname(name), 'email': email,
            'password': os.environ.get('SOCIAL_SECRET')}
        user = CustomUser.objects.create_user(**user)
        user.is_active = True
        user.auth_provider = provider
        user.save()

        new_user = authenticate(
            email=email, password=os.environ.get('SOCIAL_SECRET'))
        try:
            token = Token.objects.get(user=new_user)
        except Token.DoesNotExist:
            token = Token.objects.create(user=new_user)

        return {
            'email': new_user.email,
            'nickname': new_user.nickname,
            'token': token.key
        }