from django.db import models
from django.conf import settings
# Create your models here.

class UserProfile(models.Model):

    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    company_name = models.TextField()
    address = models.TextField()
    city = models.TextField()
    state = models.TextField()
    zip_code = models.IntegerField()

