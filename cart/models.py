from django.db import models
from django.utils.safestring import mark_safe

from products.models import Product, Image, Color
from users.models import CustomUser




CHOISES_ORDER = [
    ('New', 'New'),
    ('Decorated', 'Decorated'),
    ('Сanceled', 'Сanceled')
]


# class User


class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.PROTECT)
    data = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=CHOISES_ORDER, default='New', verbose_name="Статус")



class OrderProduct(models.Model):
    quantity = models.IntegerField(null=True, blank=True, verbose_name="Количество")
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name="Заказ")
    products = models.ForeignKey(Product, on_delete=models.PROTECT)
    image = models.ForeignKey(Image, on_delete=models.PROTECT)

    def image_tag(self):
        return mark_safe('<img src="%s" width="150" height="150" />' % (self.image.image.url))

    image_tag.short_description = 'Image'

    @property
    def price(self):
        return self.products.price

    @property
    def new_price(self):
        return self.products.new_price

    @property
    def size_range(self):
        return self.products.size_range

    @property
    def color(self):
        return self.image.color


class OrderInfo(models.Model):
    quantity = models.IntegerField()
    price = models.IntegerField()
    total_price = models.IntegerField()
    order = models.ForeignKey(Order,  on_delete=models.CASCADE)

