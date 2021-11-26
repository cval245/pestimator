from django.db import models

# Create your models here.
from django.db.models import Q


class ApplType(models.Model):
    application_type = models.CharField(default='', max_length=100)
    long_name = models.CharField(default='', max_length=100)
    internal_bool = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['application_type'],
                name='applicationTypeUniqueConstraint'),
        ]


class EPValidationTranslationRequired(models.Model):
    name = models.CharField(max_length=200)
    applicable_bool = models.BooleanField(default=False)


class EntitySize(models.Model):
    entity_size = models.CharField(max_length=30)
    description = models.CharField(max_length=200)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['entity_size'],
                name='entitySizeUniqueConstraint'),
            # models.UniqueConstraint(fields='currency_name', name='unique_currency_name')
        ]


class DocFormat(models.Model):
    name = models.CharField(default='', max_length=100)


class Country(models.Model):
    country = models.CharField(default='', max_length=100)
    active_bool = models.BooleanField(default=False)
    ep_bool = models.BooleanField(default=False)  # is country EPO member
    pct_ro_bool = models.BooleanField(default=False)  # can country be designated as receiving office for pct
    pct_accept_bool = models.BooleanField(default=False)  # can accept pcts through national phase
    # currency_name is needed for lookup when setting currency in country
    currency_name = models.CharField(default='', max_length=5)
    long_name = models.CharField(default='', max_length=100)
    color = models.CharField(default='', max_length=20)
    available_appl_types = models.ManyToManyField(ApplType)
    isa_countries = models.ManyToManyField('self')
    ep_validation_translation_required = models.ForeignKey(EPValidationTranslationRequired,
                                                           on_delete=models.CASCADE)
    entity_size_available = models.BooleanField(default=False)
    available_entity_sizes = models.ManyToManyField(EntitySize)
    available_doc_formats = models.ManyToManyField(DocFormat,
                                                   through='DocFormatCountry',
                                                   through_fields=('country', 'doc_format'),
                                                   related_name='avail_doc_formats')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['country'],
                name='uniqueCountry'),
            # models.UniqueConstraint(fields='currency_name', name='unique_currency_name')
        ]


class DocFormatCountry(models.Model):
    doc_format = models.ForeignKey(DocFormat, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    default = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['doc_format', 'country'],
                name='DocFormatCountryUniqueConstraint'
            ),
            models.UniqueConstraint(
                fields=['country'],
                condition=Q(default=True),
                name='DocFormatCountryUniqueDefaultConstraint'
            )
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

class Languages(models.Model):
    name = models.CharField(max_length=50)
    country = models.ManyToManyField(Country)
    words_per_page = models.IntegerField()
