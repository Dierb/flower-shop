from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from users.models import CustomUser


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


class Color(models.Model):
    color = models.CharField(max_length=255)

    def __str__(self):
        return self.color


class Image(models.Model):
    image = models.ImageField()


class Product(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=False, blank=True)
    details_and_care = models.TextField(null=False, blank=True)
    time_create = models.DateTimeField(auto_now_add=True)
    price = models.IntegerField(default=1)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    visits = models.IntegerField(default=0)
    image = models.ManyToManyField(Image, null=False, blank=True)
    color = models.ManyToManyField(Color, null=False, blank=True)
    size = models.CharField(max_length=5)

    def __str__(self):
        return self.name


