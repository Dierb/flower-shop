from django.contrib import admin
from django.urls import path, include
from cart.cart import Cart
from .views import CartAddAPIView, CartListAPIView, CartDeleteAPIView, CartClearAPIView, OrderAPIView
urlpatterns = [
    path("cart/", CartListAPIView.as_view()),
    path("cart/add/", CartAddAPIView.as_view()),
    path("cart/delete/<int:id>", CartDeleteAPIView.as_view()),
    path("cart/clear/", CartClearAPIView.as_view()),
    path("cart/order/", OrderAPIView.as_view()),
]
