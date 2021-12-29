import requests
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(unique=True)
    admin_data = models.BooleanField(default=False)
    terms_agreed = models.BooleanField(default=False)
    recaptcha = models.CharField(max_length=1000, default='')

    REQUIRED_FIELDS = ['email', 'terms_agreed', 'recaptcha']

#
# class Group(models.Model):
#     name = models.CharField(max_length=200, default='')
#     user = models.ManyToManyField(User)
