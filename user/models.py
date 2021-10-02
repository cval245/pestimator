from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True)
    admin_data = models.BooleanField(default=False)
    terms_agreed = models.BooleanField(default=False)

    REQUIRED_FIELDS = ['email', 'terms_agreed']
