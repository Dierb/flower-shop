from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from users.models import CustomUser
from colorfield.fields import ColorField

# Create your models here.


CHOICES = (
    (1, '★☆☆☆☆'),
    (2, '★★☆☆☆'),
    (3, '★★★☆☆'),
    (4, '★★★★☆'),
    (5, '★★★★★')
)


class Review(models.Model):
    text = models.TextField(null=True, blank=False)
    stars = models.IntegerField(default=3, choices=CHOICES)
    time_create = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=False, blank=True)
    details_and_care = models.TextField(null=False, blank=True)
    time_create = models.DateTimeField(auto_now_add=True)
    price = models.IntegerField(default=1)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    visits = models.IntegerField(default=0)
    size = models.CharField(max_length=5)

    def __str__(self):
        return self.name

    @property
    def get_color(self):
        colors = Color.objects.filter(product=self)
        return [{"color": i.color} for i in colors]

    @property
    def get_image(self):
        images = Image.objects.filter(product=self)
        return [{"id": i.id, "image": i.image.url} for i in images]


class Image(models.Model):
    image = models.ImageField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


class Color(models.Model):
    color = ColorField(default="#F0000")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.color




