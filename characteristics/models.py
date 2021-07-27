from django.db import models

# Create your models here.
class ApplType(models.Model):
    application_type = models.CharField(default='', max_length=100)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['application_type'],
                name='applicationTypeUniqueConstraint'),
            # models.UniqueConstraint(fields='currency_name', name='unique_currency_name')
        ]

class Country(models.Model):
    country = models.CharField(default='', max_length=100)
    active_bool = models.BooleanField(default=False)
    ep_bool = models.BooleanField(default=False)  # is country EPO member
    pct_analysis_bool = models.BooleanField(default=False)  # does country analyze pct
    # currency_name is needed for lookup when setting currency in country
    currency_name = models.CharField(default='', max_length=5)
    long_name = models.CharField(default='', max_length=100)
    color = models.CharField(default='', max_length=20)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['country'],
                name='uniqueCountry'),
            # models.UniqueConstraint(fields='currency_name', name='unique_currency_name')
        ]


class EntitySize(models.Model):
    entity_size = models.CharField(max_length=30)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['entity_size'],
                name='entitySizeUniqueConstraint'),
            # models.UniqueConstraint(fields='currency_name', name='unique_currency_name')
        ]

# deprecated TODO remove
class OfficeActionType(models.Model):
    oa_bool = models.BooleanField()
    name = models.CharField(max_length=50)

class OANumPerCountry(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    oa_num = models.IntegerField(default=2)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['country'],
                name='countryOANumUniqueConstraint'),
        ]

