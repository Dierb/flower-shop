from django.db.models import F
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated

from .models import Review, Category, Product
from .serializers import (ReviewSerializer, CategorySerializer, ProductSerializer,
                          ProductDetailSerializer, ReviewCreateSerializer)


class ReviewPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 100


class ReviewListAPIView(ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    pagination_class = ReviewPagination


class ReviewCreateAPIView(CreateAPIView):
    serializer_class = ReviewCreateSerializer
    permission_classes = (IsAuthenticated, )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.request.user)

        return Response({"post": serializer.data})


class CategoryListAPIView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryProductsAPIView(APIView):

    def get(self, request, id):
        try:
            queryset = Category.objects.get(id=id)
        except:
            return Response(data={"errors": "Category not found"}, status=404)
        product = Product.objects.all().filter(category_id__id=id)
        paginator = PageNumberPagination()
        paginator.page_size = 15
        result_page = paginator.paginate_queryset(product, request)
        serializers = ProductSerializer(result_page, many=True)
        serializer = CategorySerializer(queryset)
        return paginator.get_paginated_response({"category": serializer.data,
                                                 "products": serializers.data})


class ProductAPIView(APIView):
    filter_backends = (SearchFilter,)
    search_fields = ('name',)

    def filter_queryset(self, queryset):
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)
        return queryset

    def get_queryset(self):
        return Product.objects.all()

    def get(self, request):
        filtered_queryset = self.filter_queryset(self.get_queryset())
        paginator = PageNumberPagination()
        paginator.page_size = 15
        result_page = paginator.paginate_queryset(filtered_queryset, request)
        serializer = ProductSerializer(result_page, many=True)
        return paginator.get_paginated_response({
            "product": serializer.data
        })


class BestProductAPIView(APIView):

    def get(self, request):
        queryset = Product.objects.all().order_by('-visits')
        paginator = PageNumberPagination()
        paginator.page_size = 15
        result_page = paginator.paginate_queryset(queryset, request)
        serializers = ProductSerializer(result_page, many=True)
        return paginator.get_paginated_response({
                                                 "product": serializers.data
                                                 })


class ProductDetailAPIView(APIView):

    def get(self, request, id):
        queryset = Product.objects.get(id=id)
        Product.objects.filter(pk=queryset.id).update(visits=F('visits') + 1)
        serializer = ProductDetailSerializer(queryset)
        return Response({
            "product": serializer.data
        })


