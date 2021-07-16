from django.db import models

# Create your models here.
class ApplType(models.Model):
    application_type = models.CharField(default='', max_length=100)


class Country(models.Model):
    country = models.CharField(default='', max_length=100)
    active_bool = models.BooleanField(default=False)
    # currency_name is needed for lookup when setting currency in country
    currency_name = models.CharField(default='', max_length=5)


class EntitySize(models.Model):
    entity_size = models.CharField(max_length=30)


class OfficeActionType(models.Model):
    oa_bool = models.BooleanField()
    name = models.CharField(max_length=50)

class OANumPerCountry(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    oa_num = models.IntegerField(default=2)
