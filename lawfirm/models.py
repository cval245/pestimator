from django.db import models
from django.conf import settings
from djmoney.models.fields import MoneyField
from djmoney.money import Money
from characteristics.models import Country

# Create your models here.
from lawfirm.managers import LawFirmManager


# class LawFirmImages(models.Model):
#     location = models.CharField(max_length=255)


class LawFirm(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    website = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    long_description = models.TextField()
    # image_location = models.ForeignKey(LawFirmImages, on_delete=models.CASCADE)
    image_location = models.CharField(max_length=255, default='default')
    objects = LawFirmManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name'],
                name='LawFirmNameUniqueConstraint'),
            models.UniqueConstraint(
                fields=['slug'],
                name='LawFirmSlugUniqueConstraint'),
        ]


class DefaultLawFirm(models.Model):
    name = models.TextField()
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    long_description = models.TextField()
