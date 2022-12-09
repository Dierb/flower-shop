from django.shortcuts import render, get_object_or_404
from rest_framework.generics import CreateAPIView

from .models import Product, Order, OrderInfo, OrderProduct
from rest_framework.views import APIView
from .cart import Cart
from .serializers import ProductSerializer, CartAddSerializer
from rest_framework.response import Response
from users.models import CustomUser


class CartListAPIView(APIView):

    def get(self, request):
        cart = Cart(request)
        total_price = cart.get_total_price()
        ids = cart.get_product()
        products = Product.objects.filter(id__in = ids)
        products_s = ProductSerializer(products, many = True, context={"cart": cart.cart}).data

        return Response(data = {"products": products_s, "total_price": total_price})


class CartAddAPIView(CreateAPIView):
    serializer_class = CartAddSerializer

    def post(self, request, **kwargs):
        cart = Cart(request)
        id = request.data["id"]
        image_id = request.data['image_id']
        product = get_object_or_404(Product, id=id)
        cart.add(product=product, image_id=image_id)
        return Response(data={"message": "ok"})


class CartClearAPIView(APIView):

    def get(self, request):
        cart = Cart(request)
        cart.clear()
        return Response(data={"message": "clear cart"})


class CartDeleteAPIView(APIView):
    def post(self, request, id):
        cart = Cart(request)
        product =get_object_or_404(Product, id=id)
        cart.remove(product=product)
        return Response(data={"massage": "ok"})


class CartAddOrderAPIView(APIView):
    serializer = CartAddSerializer

    def post(self, request):
        cart = Cart(request)
        id = request.data["id"]
        product = get_object_or_404(Product, id=id)
        quantity = request.data['quantity']
        data = cart.update(product=product, quantity=quantity)
        return Response(data={"massage": "ok"})


class OrderAPIView(CreateAPIView):
    queryset = Order.objects.all()
    # serializer_class = OrderSerializer

    def post(self, request, *args, **kwargs):
        # serializer = self.get_serializer(data=request.data)
        # if not serializer.is_valid():
        #     return Response(data={'errors': serializer.errors})
        cart = Cart(request)
        user = CustomUser.objects.get(id=request.user.id)
        order = Order.objects.create(user=user)
        price = cart.get_total_price()
        prices = price['price']
        quantity = price['quantity']
        OrderInfo.objects.create(order_id=order.id, price=prices, total_price=prices, quantity=quantity)
        for k in cart.cart.keys():
            for i in cart.cart[k]['image'].keys():
                OrderProduct.objects.create(order_id=order.id, image_id=int(i), products_id=k, quantity=quantity)

        return Response(data={"massage": "ok"})

