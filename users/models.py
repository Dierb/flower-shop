from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class EmailAddress(models.Model):
    email = models.CharField(max_length=100)
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, related_name='email_user')
    verified = models.BooleanField(default=False)
