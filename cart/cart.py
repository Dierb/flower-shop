from django.conf import settings


class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def add(self, id, quitity, price):
        id = str(id)
        self.cart[id] = {"quitity": quitity, "price": price}
        self.save()

    def get_product(self):
        return self.cart.keys()

    
        


