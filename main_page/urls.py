from django.urls import path

from .views import (HeaderAPIView, BannerAPIView, AboutusAPIView, SaleAPIView, ReviewsAPIView, BestsellersAPIView,
                    CatalogsAPIView, FooterAPIView)


urlpatterns = [
    path('api/v1/main_page/header/', HeaderAPIView.as_view()),
    path('api/v1/main_page/banner/', BannerAPIView.as_view()),
    path('api/v1/main_page/abaut_us/', AboutusAPIView.as_view()),
    path('api/v1/main_page/sale/', SaleAPIView.as_view()),
    path('api/v1/main_page/reviews/', ReviewsAPIView.as_view()),
    path('api/v1/main_page/best_sallers', BestsellersAPIView.as_view()),
    path('api/v1/main_page/catalogs/', CatalogsAPIView.as_view()),
    path('api/v1/main_page/footer/', FooterAPIView.as_view()),
]