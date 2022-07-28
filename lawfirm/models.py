from django.db import models
from djmoney.models.fields import MoneyField
from djmoney.money import Money

from characteristics.models import ApplType, Country, DetailedFeeCategory, LawFirmFeeType

# Create your models here.
from lawfirm.managers import LawFirmManager
from user.models import User


class LawFirm(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    website = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    long_description = models.TextField()
    image_location = models.ImageField(upload_to='lawfirm')
    display_bool = models.BooleanField(default=True)

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


class LawFirmFees(models.Model):
    lawfirm = models.ForeignKey(LawFirm, on_delete=models.CASCADE)
    fee_type = models.ForeignKey(LawFirmFeeType, on_delete=models.CASCADE)
    fee_amount = MoneyField(max_digits=19,
                            decimal_places=4,
                            default=Money(0, 'USD'),
                            default_currency='USD')
