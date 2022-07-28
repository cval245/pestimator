import requests
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser

from lawfirm.models import LawFirm


class User(AbstractUser):
    email = models.EmailField(unique=True)
    admin_data = models.BooleanField(default=False)
    lawfirm = models.ForeignKey(LawFirm, on_delete=models.CASCADE)
    lawfirm_submit_data_access = models.BooleanField(default=False)
    terms_agreed = models.BooleanField(default=False)
    recaptcha = models.CharField(max_length=1000, default='')

    REQUIRED_FIELDS = ['email', 'terms_agreed', 'recaptcha']
