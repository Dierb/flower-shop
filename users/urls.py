from django.contrib import admin
from django.urls import path

from .views import (
    RegisterAPIView, activate, authorization_view, LogoutAPIView, UserAPIView,
    RestorePasswordAPIView, RestorePasswordConfirmAPIView, ChangePasswordView
)

urlpatterns = [
    path('register/', RegisterAPIView.as_view()),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',
         activate, name='activate'),
    path('authorization/', authorization_view),
    path('logout/', LogoutAPIView.as_view()),
    path('user/', UserAPIView.as_view()),
    path('restore/', RestorePasswordAPIView.as_view()),
    path('restore_password_complete/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',
         RestorePasswordConfirmAPIView.as_view(), name='restore_password_complete'),
    path('change_password/', ChangePasswordView.as_view())
]
