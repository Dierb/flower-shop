import os

from django.contrib.auth import get_user_model, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status, exceptions, authentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, renderer_classes, authentication_classes, permission_classes
from rest_framework.generics import GenericAPIView, CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer, BrowsableAPIRenderer

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from .serializers import UserCreateSerializer, UserSerializer, LoginSerializer, \
    RestorePasswordSerializer, RestorePasswordCompleteSerialaizer, ChangePasswordSerializer, GoogleSocialAuthSerializer, \
    FacebookSocialAuthSerializer
from .token import account_activation_token
from .models import CustomUser
from .authentication import CustomAuthentication


class RegisterAPIView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserCreateSerializer
    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = CustomUser.objects.create_user(**serializer.validated_data, is_active=False)
        user.save()
        current_site = get_current_site(request)
        mail_subject = 'Activation link has been sent to your email id'
        message = render_to_string('users/acc_active_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        to_email = serializer.validated_data.get('email')
        email = EmailMessage(
            mail_subject, message, to=[to_email]
        )
        email.send()
        return Response('Please confirm your email address to complete the registration')


@api_view(['GET'])
def activate(request, uidb64, token):
    CustomUser = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return Response({'messege': 'Thank you for your email confirmation Now you can login your account.'})
    else:
        return Response({'message':'Activation link is invalid!'})


class AuthorizationAPIView(CreateAPIView):
    serializer_class = LoginSerializer

    def post(self, request, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            try:
                user = CustomUser.objects.get(email=serializer.validated_data['email'])
            except CustomUser.DoesNotExist:
                raise exceptions.AuthenticationFailed('No such user')
        else:
            raise exceptions.AuthenticationFailed('Authentication failed, please check credentials')

        if user is not None:
            try:
                token = Token.objects.get(user=user)
            except Token.DoesNotExist:
                token = Token.objects.create(user=user)
            return Response(data={'key': token.key})
        return Response(data={'user': user})


class LogoutAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        request.auth.delete()
        return Response(data={"message": "You have successfully logged out."})


class UserAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get(self, request):
        if request.auth and request.user.is_authenticated:
            user = request.user
            serializer = UserSerializer(user).data
            return Response(serializer)
        else:
            return Response(data={'message': "You are not authenticated"})


class RestorePasswordAPIView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RestorePasswordSerializer

    def post(self, request):
        serializer = RestorePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.send_password_change_form()
        else:
            Response(data=["can't send email subject to your email"])
        return Response(data={"message": "Please check your email to restore your account"})


class RestorePasswordConfirmAPIView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RestorePasswordCompleteSerialaizer

    def post(self, request, uidb64, token):
        CustomUser = get_user_model()
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            serializer = RestorePasswordCompleteSerialaizer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                user.set_password(serializer.validated_data.get('password'))
                user.save()
                print(serializer.validated_data.get('password'))
                print(user.password)
                return Response("Password changed you can log in")
        else:
            return Response({'message': 'Activation link is invalid!'})


class ChangePasswordView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def post(self, request):
        data = request.data
        serializer = ChangePasswordSerializer(data=data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.set_new_password()
            return Response('Password successfully changed!')


class GoogleSocialAuthView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = GoogleSocialAuthSerializer

    def post(self, request):
        """
        POST with "auth_token"
        Send an idtoken as from google to get user information
        """

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = ((serializer.validated_data)['auth_token'])
        return Response(data, status=status.HTTP_200_OK)


class FacebookSocialAuthView(GenericAPIView):

    serializer_class = FacebookSocialAuthSerializer

    def post(self, request):
        """
        POST with "auth_token"
        Send an access token as from facebook to get user information
        """

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = ((serializer.validated_data)['auth_token'])
        return Response(data, status=status.HTTP_200_OK)
