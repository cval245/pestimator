from django.db import models
from relativedeltafield import RelativeDeltaField

from characteristics.models import Country, ApplType, Languages


class BaseTransform(models.Model):
    date_diff = RelativeDeltaField()
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    class Meta:
        abstract = True




class CustomFilingTransform(BaseTransform):
    appl_type = models.ForeignKey(ApplType, on_delete=models.CASCADE)
    prev_appl_type = models.ForeignKey(ApplType, on_delete=models.CASCADE,
                                       null=True, related_name='prev_appl_type')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['appl_type', 'prev_appl_type', 'country'],
                name='applicationTypePrevApplTypeCountryUniqueConstraint'),
        ]


class PublicationTransform(BaseTransform):
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['country'],
                name='PublicationCountryUniqueConstraint'),
        ]

class OATransform(BaseTransform):
    # oa_num = models.IntegerField()
    pass


class USOATransform(OATransform):
    final_oa_bool = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['final_oa_bool'],
                name='FinalOABoolUniqueConstraint'),
        ]


class AllowanceTransform(BaseTransform):
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['country'],
                name='AllowanceCountryUniqueConstraint'),
        ]


class IssueTransform(BaseTransform):
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['country'],
                name='IssueCountryUniqueConstraint'),
        ]


class CountryOANum(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    oa_total = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['country'],
                name='CountryOANumCountryUniqueConstraint'),
        ]

class DefaultCountryOANum(models.Model):
    oa_total = models.IntegerField()


class BaseDefaultTransform(models.Model):
    date_diff = RelativeDeltaField()
    appl_type = models.ForeignKey(ApplType, on_delete=models.CASCADE)
    class Meta:
        abstract = True
        constraints = [
            models.UniqueConstraint(
                fields=['appl_type'],
                name='ApplTypeUniqueConstraint'),
        ]

class DefaultFilingTransform(BaseDefaultTransform):
    class Meta:
        abstract = False


class DefaultPublTransform(BaseDefaultTransform):
    class Meta:
        abstract = False



class DefaultOATransform(BaseDefaultTransform):
    class Meta:
        abstract = False


class DefaultAllowanceTransform(BaseDefaultTransform):
    class Meta:
        abstract = False


class DefaultIssueTransform(BaseDefaultTransform):
    class Meta:
        abstract = False

# class LanguageTranslation(models.Model):
#     language = models.OneToOneField(Languages, on_delete=models.CASCADE)
#     ratio_pages_to_en_pages = models.DecimalField(max_digits=5, decimal_places=2)
