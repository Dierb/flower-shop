import re
from django.shortcuts import render, get_object_or_404
from .models import Product
from rest_framework.views import APIView
from .cart import Cart
from .serializers import ProductSerializer
from rest_framework.response import Response

class CartList(APIView):
    def get(self, request):
        cart = Cart(request)
        ids = cart.get_product()
        products = Product.objects.filter(id__in = ids)
        products_s = ProductSerializer(products, many = True, context={"cart": cart}).data

        return Response(data = products_s)


class CartAdd(APIView):
    def post(self,request, id):
        cart = Cart(request)
        product = get_object_or_404(Product, id = id)
        cart.add(id = product.id, quitity=1 , price = product.price)
        return Response(data= {"message": "ok"})





