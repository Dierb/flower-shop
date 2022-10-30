from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

# Create your models here.


class CustomBaseUserManager(BaseUserManager):

    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    email = models.EmailField(verbose_name='email', max_length=128, unique=True)
    phone_number = models.CharField(max_length=13)
    username = None
    nickname = models.CharField(max_length=128, blank=False, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('phone_number',)
    objects = CustomBaseUserManager()

    def __str__(self):
        return self.email


class EmailAddress(models.Model):
    email = models.CharField(max_length=100)
    user = models.OneToOneField(to=CustomUser, on_delete=models.CASCADE, related_name='email_user')
    verified = models.BooleanField(default=False)
