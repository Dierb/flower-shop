from django.contrib import admin
from django.urls import path, include
from cart.cart import Cart
from .views import CartAdd, CartList
urlpatterns = [
    path("cart/", CartList.as_view()),
    path("cart/add/<int:id>/", CartAdd.as_view())
]
