from django.contrib.auth import get_user_model, authenticate
from rest_framework import authentication
from rest_framework import exceptions


class CustomAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        # Get the username and password
        email = request.data.get('email', None)
        password = request.data.get('password', None)
        if not email or not password:
            raise exceptions.AuthenticationFailed('No credentials provided.')

        credentials = {
            'email': email,
            'password': password
        }

        user = authenticate(**credentials)

        if user is None:
            raise exceptions.AuthenticationFailed('Invalid username/password.')

        if not user.is_active:
            raise exceptions.AuthenticationFailed('User inactive or deleted.')

        return (user, None)