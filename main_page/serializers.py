from rest_framework import serializers
from .models import Header, Banner, About_us, Sale, Reviews, Best_sellers, Catalogs, Footer


class HeaderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Header
        fields = 'logo plants care_tools gifts learn search basket user'.split()


class BannerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Banner
        fields = 'image title description button'.split()




class SaleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sale
        fields = 'image title description'.split()


class ReviewsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reviews
        fields = 'amount title image description'.split()


class BestsellersSerializer(serializers.ModelSerializer):

    class Meta:
        model = Best_sellers
        fields = 'amount image title'.split()


class CatalogsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Catalogs
        fields = 'amount image title description'.split()


class FooterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Footer
        fields = 'background About Join_Pianta Terms descriptuion'.split()


class AboutusSerializer(serializers.ModelSerializer):

    class Meta:
        model = About_us
        fields = "image title description button".split()