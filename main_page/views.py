from django.shortcuts import render
from .models import (Header, Banner, About_us, Sale, Reviews, Best_sellers, Catalogs, Footer)
from rest_framework.generics import ListAPIView

from .serializers import (HeaderSerializer,
                          BannerSerializer,
                          AboutusSerializer,
                          SaleSerializer,
                          ReviewsSerializer,
                          BestsellersSerializer,
                          CatalogsSerializer,
                          FooterSerializer)


class HeaderAPIView(ListAPIView):
    queryset = Header.objects.all()
    serializer_class = HeaderSerializer


class BannerAPIView(ListAPIView):
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer


class AboutusAPIView(ListAPIView):
    queryset = About_us.objects.all()
    serializer_class = AboutusSerializer


class SaleAPIView(ListAPIView):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer


class ReviewsAPIView(ListAPIView):
    queryset = Reviews.objects.all()
    serializer_class = ReviewsSerializer


class BestsellersAPIView(ListAPIView):
    queryset = Best_sellers.objects.all()
    serializer_class = BestsellersSerializer


class CatalogsAPIView(ListAPIView):
    queryset = Catalogs.objects.all()
    serializer_class = CatalogsSerializer


class FooterAPIView(ListAPIView):
    queryset = Footer.objects.all()
    serializer_class = FooterSerializer

