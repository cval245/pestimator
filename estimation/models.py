from django.db import models
from application.models import UtilityApplication, BaseApplication,\
    OfficeAction, USOfficeAction, Publication, Allowance, Issue
from djmoney.models.fields import MoneyField
from djmoney.money import Money
from characteristics.models import Country, EntitySize
from relativedeltafield import RelativeDeltaField

# Create your models here.
class LineEstimationTemplateConditions(models.Model):
    condition_claims_min = models.IntegerField(blank=True, null=True)
    condition_claims_max = models.IntegerField(blank=True, null=True)
    condition_pages_min = models.IntegerField(blank=True, null=True)
    condition_pages_max = models.IntegerField(blank=True, null=True)
    condition_drawings_min = models.IntegerField(blank=True, null=True)
    condition_drawings_max = models.IntegerField(blank=True, null=True)
    condition_entity_size = models.ForeignKey(EntitySize, on_delete=models.CASCADE)

class LawFirmEstTemplate(models.Model):
    law_firm_cost = MoneyField(max_digits=19,
                               decimal_places=4,
                               default=Money(0, 'USD'),
                               default_currency='USD')
    date_diff = RelativeDeltaField()

    class Meta:
        abstract = False



class BaseEstTemplate(models.Model):
    official_cost = MoneyField(max_digits=19,
                               decimal_places=4,
                               default=Money(0, 'USD'),
                               default_currency='USD')
    date_diff = RelativeDeltaField()
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    conditions = models.ForeignKey(LineEstimationTemplateConditions, on_delete=models.CASCADE)
    law_firm_template = models.OneToOneField(LawFirmEstTemplate, on_delete=models.CASCADE, null=True)

    class Meta:
        abstract = True



class FilingEstimateTemplate(BaseEstTemplate):

    class Meta:
        abstract = False


class PublicationEstTemplate(BaseEstTemplate):

    class Meta:
        abstract = False


class OAEstimateTemplate(BaseEstTemplate):

    class Meta:
        abstract = False


class USOAEstimateTemplate(OAEstimateTemplate):
    oa_type = models.CharField(max_length=20)

    class Meta:
        abstract = False


class AllowanceEstTemplate(BaseEstTemplate):

    class Meta:
        abstract = False


class IssueEstTemplate(BaseEstTemplate):

    class Meta:
        abstract = False


# ********************************************************
#  Estimates below
#
# ********************************************************

class LawFirmEst(models.Model):
    law_firm_cost = MoneyField(max_digits=19,
                               decimal_places=4,
                               default=Money(0, 'USD'),
                               default_currency='USD')
    date = models.DateField()


class BaseEst(models.Model):
    official_cost = MoneyField(max_digits=19,
                               decimal_places=4,
                               default=Money(0, 'USD'),
                               default_currency='USD')
    date = models.DateField()
    law_firm_est = models.OneToOneField(LawFirmEst, on_delete=models.CASCADE, null=True)
    application = models.ForeignKey(BaseApplication,
                                    on_delete=models.CASCADE)
    class Meta:
        abstract = False



class FilingEstimate(BaseEst):
    
    class Meta:
        abstract = False


class OAEstimate(BaseEst):
    office_action = models.ForeignKey(OfficeAction,
                                      on_delete=models.CASCADE)

    class Meta:
        abstract = False

class USOAEstimate(BaseEst):
    office_action = models.ForeignKey(USOfficeAction,
                                        on_delete=models.CASCADE)


class PublicationEst(BaseEst):
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE)

    class Meta:
        abstract = False


class AllowanceEst(BaseEst):
    allowance = models.ForeignKey(Allowance, on_delete=models.CASCADE)

    class Meta:
        abstract = False


class IssueEst(BaseEst):
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)

    class Meta:
        abstract = False

