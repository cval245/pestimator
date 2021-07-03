from django.db import models
from django.conf import settings
from djmoney.models.fields import MoneyField
from djmoney.money import Money
from characteristics.models import Country

# Create your models here.


class LawFirm(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    name = models.TextField()
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    hourly = MoneyField(max_digits=19,
                        decimal_places=4,
                        default=Money(0, 'USD'),
                        default_currency='USD')

class DefaultLawFirm(models.Model):
    name = models.TextField()
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    hourly = MoneyField(max_digits=19,
                        decimal_places=4,
                        default=Money(0, 'USD'),
                        default_currency='USD')
