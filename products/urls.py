from django.urls import path
from . import views


urlpatterns = [
    path("api/v1/review/", views.ReviewListAPIView.as_view()),
    path("api/v1/review/create/", views.ReviewCreateAPIView.as_view()),
    path("api/v1/category/", views.CategoryListAPIView.as_view()),
    path("api/v1/category/<int:id>/", views.CategoryProductsAPIView.as_view()),
    path("api/v1/product/", views.ProductAPIView.as_view()),
    path("api/v1/product/best/", views.BestProductAPIView.as_view()),
    path("api/v1/product/<int:id>/", views.ProductDetailAPIView.as_view()),
]