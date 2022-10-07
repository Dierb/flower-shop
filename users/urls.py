from django.contrib import admin
from django.urls import path

from .views import (
    RegisterAPIView, activate, authorization_view
)

urlpatterns = [
    path('register/', RegisterAPIView.as_view()),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',
         activate, name='activate'),
    path('authorization/', authorization_view)
]
