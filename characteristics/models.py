from django.db import models

# Create your models here.
from django.db.models import Q, Count, F

from characteristics.managers import TranslationImplementedPseudoEnumManager, ApplTypesEnumManager
from characteristics.enums import TranslationRequirements, ApplTypes


class Language(models.Model):
    name = models.CharField(max_length=50)
    words_per_page = models.IntegerField()
    ep_official_language_bool = models.BooleanField(default=False)


class ApplType(models.Model):
    application_type = models.CharField(default='', max_length=100)
    long_name = models.CharField(default='', max_length=100)
    internal_bool = models.BooleanField(default=True)

    objects = ApplTypesEnumManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['application_type'],
                name='applicationTypeUniqueConstraint'),
        ]

    def get_enum(self):
        if self.application_type == 'utility':
            return ApplTypes.UTILITY
        elif self.application_type == 'nationalphase':
            return ApplTypes.PCT_NATIONAL_PHASE
        elif self.application_type == 'epvalidation':
            return ApplTypes.EP_VALIDATION
        elif self.application_type == 'pct':
            return ApplTypes.PCT
        elif self.application_type == 'ep':
            return ApplTypes.EP
        elif self.application_type == 'prov':
            return ApplTypes.PROV
        return ApplTypes.UTILITY


class EPValidationTranslationRequired(models.Model):
    # London Treaty for EP Applications
    name = models.CharField(max_length=200)
    # applicable_bool = models.BooleanField(default=False)

class TranslationRequiredOptions(models.Model):
    name = models.CharField(max_length=200)

class TranslationImplementedPseudoEnum(models.Model):
    name = models.CharField(max_length=200)

    objects = TranslationImplementedPseudoEnumManager()

    def get_enum(self):
        if self.name == 'no translation':
            return TranslationRequirements.NO_TRANSLATION
        elif self.name == 'full translation':
            return TranslationRequirements.FULL_TRANSLATION
        elif self.name == 'claims translation':
            return TranslationRequirements.CLAIMS_TRANSLATION


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
    ep_validation_translation_required = models.ForeignKey(
        EPValidationTranslationRequired,
        on_delete=models.CASCADE)  # London Agreement
    utility_translation_required = models.ForeignKey(
        TranslationRequiredOptions,
        on_delete=models.PROTECT
    )
    available_doc_formats = models.ManyToManyField(DocFormat,
                                                   through='DocFormatCountry',
                                                   through_fields=('country', 'doc_format', 'appl_type'),
                                                   related_name='available_doc_formats')
    available_languages = models.ManyToManyField(Language,
                                                 through='LanguageCountry',
                                                 through_fields=('country', 'language', 'appl_type'),
                                                 related_name='available_languages')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['country'],
                name='uniqueCountry'),
            # models.UniqueConstraint(fields='currency_name',
            # name='unique_currency_name')
        ]

    def get_country_formats(self):
        return DocFormatCountry.objects.filter(country=self)

    def get_languages(self):
        return LanguageCountry.objects.filter(country=self)

    # def get_paris_country_customization(self,):


class EntitySize(models.Model):
    entity_size = models.CharField(max_length=30)
    description = models.CharField(max_length=200)
    default_bool = models.BooleanField(default=False)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['entity_size', 'country'],
                name='entitySizeCountryUniqueConstraint'),
            models.UniqueConstraint(
                fields=['country'],
                condition=Q(default_bool=True),
                name='DefaultEntitySizeCountryUniqueConstraint'),
        ]


class DocFormatCountry(models.Model):
    doc_format = models.ForeignKey(DocFormat, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    appl_type = models.ForeignKey(ApplType, on_delete=models.CASCADE)
    default = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['doc_format', 'country', 'appl_type'],
                name='DocFormatCountryUniqueConstraint',
            ),
            models.UniqueConstraint(
                fields=['country', 'appl_type'],
                condition=Q(default=True),
                name='DocFormatCountryUniqueDefaultConstraint',
            )
        ]


class LanguageCountry(models.Model):
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    appl_type = models.ForeignKey(ApplType, on_delete=models.CASCADE)
    default = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['language', 'country', 'appl_type'],
                name='LanguageCountryUniqueConstraint',
            ),
            models.UniqueConstraint(
                fields=['language', 'country', 'appl_type'],
                condition=Q(default=True),
                name='LanguageCountryUniqueDefaultConstraint',
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


class FeeCategory(models.Model):
    name = models.CharField(max_length=200)


class DetailedFeeCategory(models.Model):
    name = models.CharField(max_length=200)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    appl_types = models.ManyToManyField(ApplType)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'country'],
                name='UniqueNameCountryConstraint')
        ]
