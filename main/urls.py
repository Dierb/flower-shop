from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .yasg import ulrpatterns as doc_urls
from products import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/v1/review/", views.ReviewListAPIView.as_view()),
    path("api/v1/review/create/", views.ReviewCreateAPIView.as_view()),
    path("api/v1/category/", views.CategoryListAPIView.as_view()),
    path("api/v1/category/<int:id>/", views.CategoryProductsAPIView.as_view()),
    path("api/v1/product/", views.ProductAPIView.as_view()),
    path("api/v1/product/best/", views.BestProductAPIView.as_view()),
    path("api/v1/product/<int:id>/", views.ProductDetailAPIView.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += doc_urls
