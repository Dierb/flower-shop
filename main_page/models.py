from django.db import models
from pydoc import describe


class Header(models.Model):
    logo = models.ImageField()
    plants = models.CharField(max_length=20)
    care_tools = models.CharField(max_length=20)
    gifts = models.CharField(max_length=20)
    learn = models.CharField(max_length=20)
    search = models.ImageField()
    basket = models.ImageField()
    user = models.ImageField()
    

class Banner(models.Model):
    image = models.ImageField()
    title = models.CharField(max_length=40)
    description = models.TextField(null=False, blank=True)
    button = models.CharField(max_length=20)


class About_us(models.Model):
    image = models.ImageField()
    title = models.CharField(max_length=40)
    description = models.TextField(null=False, blank=True)
    button = models.CharField(max_length=20)


class Sale(models.Model):
    image = models.ImageField()
    title = models.CharField(max_length=40)
    description = models.TextField(null=False, blank=True)


class Best_sellers(models.Model):
    amount = models.PositiveIntegerField()
    image = models.ImageField()
    title = models.CharField(max_length=40)



class Catalogs(models.Model):
    amount = models.PositiveIntegerField()
    image = models.ImageField()
    title = models.CharField(max_length=40)
    description = models.TextField(null=False, blank=True)


class Reviews(models.Model):
    amount = models.PositiveIntegerField()
    title = models.CharField(max_length=40)
    image = models.ImageField()
    description = models.TextField(null=False, blank=True)


class Footer(models.Model):
    background = models.ImageField(upload_to='')
    About = models.CharField(max_length=20)
    Join_Pianta = models.CharField(max_length=20)
    Terms = models.CharField(max_length=20)
    descriptuion = models.TextField(null=False, blank=True)
