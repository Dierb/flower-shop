from django.db import models
from pydoc import describe
from unittest.util import _MAX_LENGTH

class Header(models.Model):
    logo = models.ImageField(upload_to='')
    plants = models.CharField(max_length=20)
    care_tools = models.CharField(max_length=20)
    gifts = models.CharField(max_length=20)
    learn = models.CharField(max_length=20)
    search = models.ImageField(upload_to='')
    basket = models.ImageField(upload_to='')
    user = models.ImageField(upload_to='')
    

class Banner(models.Model):
    image = models.ImageField(upload_to='')
    title = models.CharField(max_length=40)
    description = models.TextField
    button = models.CharField(max_length=20)


class About_us(models.Model):
    image = models.ImageField(upload_to='')
    title = models.CharField(max_length=40)
    description = models.TextField
    button = models.CharField(max_length=20)


class Sale(models.Model):
    image = models.ImageField(upload_to='')
    title = models.CharField(max_length=40)
    description = models.TextField


class Best_sellers(models.Model):
    amount = models.PositiveIntegerField()
    image = models.ImageField(upload_to='')
    title = models.CharField(max_length=40)



class Catalogs(models.Model):
    amount = models.PositiveIntegerField()
    image = models.ImageField(upload_to='')
    title = models.CharField(max_length=40)
    description = models.TextField


class Reviews(models.Model):
    amount = models.PositiveIntegerField()
    title = models.CharField(max_length=40)
    image = models.ImageField(upload_to='')
    description = models.TextField


class Footer(models.Model):
    background = models.ImageField(upload_to='')
    About = models.CharField(max_length=20)
    Join_Pianta = models.CharField(max_length=20)
    Terms = models.CharField(max_length=20)
    descriptuion = models.TextField
