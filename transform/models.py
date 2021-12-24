from django.db import models
from relativedeltafield import RelativeDeltaField

from characteristics.models import Country, ApplType, Language
from transform.managers import FilingTransformManager


class TransComplexTime(models.Model):
    name = models.CharField(max_length=200)

    def calc_complex_time_conditions(self, prev_date, filing_transform, prev_appl_option):
        if self.name == 'from priority date':
            return self.calc_from_priority_date(prev_appl_option=prev_appl_option, prev_date=prev_date,
                                                filing_transform=filing_transform)

    def calc_from_priority_date(self, prev_appl_option, prev_date, filing_transform):
        if prev_appl_option is None:
            return prev_date + filing_transform.date_diff

        new_date = prev_appl_option.date_filing + filing_transform.date_diff
        appl = prev_appl_option
        while appl is not None:
            prior_appl_option = appl.prev_appl_options
            if prior_appl_option is None:
                # get the date
                priority_date = appl.date_filing
                new_date = priority_date + filing_transform.date_diff
            appl = prior_appl_option
            # traverse to the top of the tree
        return new_date


class BaseTransform(models.Model):
    date_diff = RelativeDeltaField()
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    trans_complex_time_condition = models.ForeignKey(TransComplexTime,
                                                     on_delete=models.CASCADE,
                                                     null=True, default=None)
    appl_type = models.ForeignKey(ApplType, on_delete=models.CASCADE)

    class Meta:
        abstract = True



class CustomFilingTransform(BaseTransform):
    prev_appl_type = models.ForeignKey(ApplType, on_delete=models.CASCADE,
                                       null=True, related_name='prev_appl_type')

    objects = FilingTransformManager()
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
                fields=['country', 'appl_type'],
                name='PublicationCountryApplTypeUniqueConstraint'),
        ]


class RequestExaminationTransform(BaseTransform):
    pass


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
                fields=['country', 'appl_type'],
                name='AllowanceCountryApplTypeUniqueConstraint'),
        ]


class IssueTransform(BaseTransform):
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['country', 'appl_type'],
                name='IssueCountryApplTypeUniqueConstraint'),
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
                name='App%(class)s'),
        ]


class DefaultFilingTransform(BaseDefaultTransform):
    pass
    # class Meta:
    #     abstract = False


class DefaultRequestExaminationTransform(BaseDefaultTransform):
    pass
    # class Meta:
    #     abstract = False


class DefaultPublTransform(BaseDefaultTransform):
    pass
    # class Meta:
    #     abstract = False


class DefaultOATransform(BaseDefaultTransform):
    pass
    # class Meta:
    #     abstract = False


class DefaultAllowanceTransform(BaseDefaultTransform):
    pass
    # class Meta:
    #     abstract = False


class DefaultIssueTransform(BaseDefaultTransform):
    pass
    # class Meta:
    #     abstract = False

# class LanguageTranslation(models.Model):
#     language = models.OneToOneField(Language, on_delete=models.CASCADE)
#     ratio_pages_to_en_pages = models.DecimalField(max_digits=5, decimal_places=2)
