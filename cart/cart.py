from decimal import Decimal

from django.conf import settings

from cart.models import Image


class Cart(object):
    def __init__(self, request):
        """Инициализация коризны"""
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def add(self, product, color, quantity=1, update_quantity=False):
        """Добавление и обновление товара в карзине"""
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0,
                                     'price': str(product.price),
                                     'color': {color: 0},
                                     }

        if product_id in self.cart and color not in self.cart[product_id]["color"]:
            self.cart[product_id]['color'][color] = 0


        if update_quantity:
            self.cart[product_id]['quantity'] -= self.cart[product_id]['color'][color]
            self.cart[product_id]['color'][color] = quantity
            self.cart[product_id]['quantity'] += quantity
        else:
            print(self.cart[product_id]['color'][color])
            self.cart[product_id]['quantity'] += quantity
            self.cart[product_id]['color'][color] += quantity
            print(self.cart[product_id]['color'][color])
        self.save()

    def remove(self, product):
        """Удалине товара"""
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        price = sum(Decimal(item['price']) * item['quantity'] for item in
                    self.cart.values())

        quantity = sum(Decimal(1) * item['quantity'] for item in
                       self.cart.values())

        return {"price": price, "quantity": quantity}

    def clear(self):
        """Очистка коризны"""
        # удаление корзины из сессии
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True

    def get_product(self):
        return self.cart.keys()
