from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

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
        color = request.data['color']
        product = get_object_or_404(Product, id=id)
        # if image_id in cart.cart[str(id)]['color'].keys():
        #     update_quantity = True
        # else:
        #     update_quantity = False
        cart.add(product=product, color=color)
        return Response(data={"message": "ok"})


# class UpdateCartAPIView(CreateAPIView):
#     serializer_class = CartAddSerializer
#
#     def post(self, request, **kwargs):
#         cart = Cart(request)
#         id = request.data["id"]
#         image_id = request.data['image_id']
#         product = get_object_or_404(Product, id=id)
#         if id not in cart.cart[str(id)].keys():
#
#         # if image_id in cart.cart[str(id)]['color'].keys():
#         #     update_quantity = True
#         # else:
#         #     update_quantity = False
#         cart.add(product=product, color=image_id)
#         return Response(data={"message": "ok"})

class CartClearAPIView(APIView):

    def get(self, request):
        cart = Cart(request)
        cart.clear()
        return Response(data={"message": "ok"})


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
    permission_classes = (IsAuthenticated, )

    # def get_serializer_class(self):
    #     return OrderSerializer

    def post(self, request, *args, **kwargs):
        # serializer = self.get_serializer(data=request.data)
        # if not serializer.is_valid():
        #     return Response(data={'errors': serializer.errors})
        if request.user.is_authenticated:
            cart = Cart(request)
            if len(cart) == 0:
                return Response(data={"massage": "cart is empty"})
            user = CustomUser.objects.get(id=request.user.id)
            order = Order.objects.create(user=user)
            price = cart.get_total_price()
            prices = price['price']
            quantity = price['quantity']
            OrderInfo.objects.create(order_id=order.id, price=prices, total_price=prices, quantity=quantity)
            for k in cart.cart.keys():
                for i in cart.cart[k]['color'].keys():
                    OrderProduct.objects.create(order_id=order.id, color=i, products_id=k, quantity=cart.cart[k]["color"][i])
            cart.cart.clear()

            return Response(data={"massage": "ok"})
        else:
            return Response(data={"redirect_to":"http:127:0.0.1:8000/api/v1/users/authorization/"})


