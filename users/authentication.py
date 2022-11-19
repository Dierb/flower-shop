from django.contrib.auth import get_user_model, authenticate
from rest_framework import authentication
from rest_framework import exceptions
from rest_framework.authentication import TokenAuthentication


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
