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

    def save(self, *args, **kwargs):
        if settings.USE_RECAPTCHA_BOOL:
            # Recaptcha validation
            url = 'https://www.google.com/recaptcha/api/siteverify'
            values = {
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': self.recaptcha
            }
            r = requests.post(url, data=values)
            rjson = r.json()
            if (rjson['success'] == True):
                super(User, self).save(*args, **kwargs)
        else:
            # not recaptcha for testing only
            super(User, self).save(*args, **kwargs)
