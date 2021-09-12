import math

from django.db import models
from djmoney.contrib.exchange.models import convert_money
from djmoney.models.fields import MoneyField
from djmoney.money import Money
from relativedeltafield import RelativeDeltaField

from application.models import BaseApplication, BaseUtilityApplication, USUtilityApplication
from application.models.allowance import Allowance
from application.models.issue import Issue
from application.models.officeAction import OfficeAction
from application.models.publication import Publication
from application.models.usOfficeAction import USOfficeAction
from application.models.utilityApplication import UtilityApplication
from characteristics.models import Country, EntitySize, ApplType, Languages
from estimation.managers import EstimateManager, OAEstimateManager, USOAEstimateManager, PublEstimateManager, \
    AllowanceEstimateManager, IssueEstimateManager


class ComplexTimeConditions(models.Model):
    name = models.CharField(max_length=200)

    def calc_complex_time_condition(self, application, date_diff, template_conditions):
        if (self.name == 'from priority date'):
            return self.calc_from_priority_date(application, date_diff)
        elif (self.name == 'from ep filing date'):
            return self.calc_from_date_of_parent_ep_application(application, date_diff)

        return None

    def calc_from_priority_date(self, application, date_diff):
        appl = application
        new_date = application.date_filing + date_diff
        while (appl != None):
            prior_appl = appl.prior_appl
            if (prior_appl == None):
                # get the date
                priority_date = appl.date_filing
                new_date = priority_date + date_diff
            appl = prior_appl
            # traverse to the top of the tree
            # retrieve the application date calc and then return diff from filing date
        return new_date

    def calc_from_date_of_parent_ep_application(self, application, date_diff):
        new_date = application.date_filing + date_diff
        prior_application = application.prior_appl
        if (prior_application):
            if (prior_application.appl_type
                    == ApplType.objects.get(appl_type='ep')):
                new_date = prior_application.date_filing + date_diff

        return new_date


class ComplexConditions(models.Model):
    name = models.CharField(max_length=200)

    def calc_complex_condition(self, appl_details, cost, template_conditions):
        if (self.name == 'multiply each by template above minimum indep claims'):
            return self.calc_multiply_each_by_template_above_minimum_indep_claims(appl_details,
                                                                                  template_conditions,
                                                                                  cost)
        elif (self.name == 'multiply each by template above minimum total claims'):
            return self.calc_multiply_each_by_template_above_minimum_total_claims(appl_details,
                                                                                  template_conditions,
                                                                                  cost)
        elif (self.name == 'multiply each page by unit of fifty pages'):
            return self.calc_multiply_each_by_template_above_minimum_total_claims(appl_details,
                                                                                  template_conditions,
                                                                                  cost)
        elif (self.name == 'multiply each addl page'):
            return self.calc_multiply_each_additional_page(appl_details,
                                                           template_conditions,
                                                           cost)
        elif (self.name == 'date_diff from earliest priority_date'):
            return self.calc_multiply_each_additional_page(appl_details,
                                                           template_conditions,
                                                           cost)
        return None

    def calc_multiply_each_by_template_above_minimum_indep_claims(self, appl_details,
                                                                  template_conditions,
                                                                  cost):
        # $100 per indep claim in excess of 3
        # 5 claims will yield a fee of $200
        # 7 claims will yield a fee of $400
        if (template_conditions.condition_indep_claims_min):
            num_fee_indep_claims = appl_details.num_indep_claims - template_conditions.condition_indep_claims_min
        else:
            num_fee_indep_claims = appl_details.num_indep_claims - 0
        fee = num_fee_indep_claims * cost
        return fee

    def calc_multiply_each_by_template_above_minimum_total_claims(self, appl_details,
                                                                  template_conditions,
                                                                  cost):
        # $100 per claim in excess of 20
        # 21 claims will yield a fee of $100
        if (template_conditions.condition_claims_min):
            num_fee_claims = appl_details.num_claims - template_conditions.condition_claims_min
        else:
            num_fee_claims = appl_details.num_claims
        fee = num_fee_claims * cost
        return fee

    def calc_multiply_each_page_by_unit_of_fifty_pages(self, appl_details,
                                                       template_conditions,
                                                       cost):
        # $100 per set of 50 pages in excess of 100
        # 150 pages will yield a fee of $100
        if (template_conditions.condition_pages_min):
            total_pages = appl_details.total_pages - template_conditions.condition_pages_min
            total_pages = math.floor(total_pages / 50)
        else:
            total_pages = appl_details.total_pages - 0
            total_pages = math.floor(total_pages / 50)
        fee = total_pages * cost
        return fee

    def calc_multiply_each_additional_page(self, appl_details,
                                           template_conditions,
                                           cost):
        # $100 per set of 50 pages in excess of 100
        # 150 pages will yield a fee of $100
        if (template_conditions.condition_pages_min):
            total_pages = appl_details.total_pages - template_conditions.condition_pages_min
        else:
            total_pages = appl_details.total_pages - 0
        fee = total_pages * cost
        return fee


class LineEstimationTemplateConditions(models.Model):
    condition_claims_min = models.IntegerField(blank=True, null=True)
    condition_claims_max = models.IntegerField(blank=True, null=True)
    condition_indep_claims_min = models.IntegerField(blank=True, null=True)
    condition_indep_claims_max = models.IntegerField(blank=True, null=True)
    condition_pages_min = models.IntegerField(blank=True, null=True)
    condition_pages_max = models.IntegerField(blank=True, null=True)
    condition_drawings_min = models.IntegerField(blank=True, null=True)
    condition_drawings_max = models.IntegerField(blank=True, null=True)
    condition_entity_size = models.ForeignKey(EntitySize,
                                              on_delete=models.CASCADE,
                                              null=True)
    condition_annual_prosecution_fee = models.BooleanField(default=False)
    condition_complex = models.ForeignKey(ComplexConditions,
                                          on_delete=models.CASCADE,
                                          null=True, default=None)
    condition_time_complex = models.ForeignKey(ComplexTimeConditions,
                                               on_delete=models.CASCADE,
                                               null=True, default=None)
    prior_pct = models.BooleanField(null=True)
    prior_pct_same_country = models.BooleanField(null=True)
    prev_appl_date_excl_intermediary_time = models.BooleanField(default=False)

class LawFirmEstTemplate(models.Model):
    law_firm_cost = MoneyField(max_digits=19,
                               decimal_places=4,
                               default=Money(0, 'USD'),
                               default_currency='USD')
    date_diff = RelativeDeltaField()

    # objects = TemplateManager()

    class Meta:
        abstract = False



class BaseEstTemplate(models.Model):
    official_cost = MoneyField(max_digits=19,
                               decimal_places=4,
                               default=Money(0, 'USD'),
                               default_currency='USD')
    date_diff = RelativeDeltaField()
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    appl_type = models.ForeignKey(ApplType, on_delete=models.CASCADE)

    conditions = models.OneToOneField(LineEstimationTemplateConditions, on_delete=models.CASCADE)
    law_firm_template = models.OneToOneField(LawFirmEstTemplate, on_delete=models.CASCADE)
    description = models.TextField()
    fee_code = models.CharField(max_length=30)

    # objects = TemplateManager()

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        # override so the country and currency are correct
        self.official_cost = Money(self.official_cost.amount, self.country.currency_name)
        self.law_firm_template.law_firm_cost = \
            Money(self.law_firm_template.law_firm_cost.amount, self.country.currency_name)
        self.law_firm_template.save()
        return super().save()

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
    oa_final_bool = models.BooleanField(default=False)
    oa_first_final_bool = models.BooleanField(default=False)

    class Meta:
        abstract = False


class AllowanceEstTemplate(BaseEstTemplate):
    class Meta:
        abstract = False


class IssueEstTemplate(BaseEstTemplate):
    class Meta:
        abstract = False


class TranslationEstTemplate(models.Model):
    start_language = models.ForeignKey(Languages, on_delete=models.CASCADE, related_name='start_language_est_temp')
    end_language = models.ForeignKey(Languages, on_delete=models.CASCADE, related_name='end_language_est_temp')
    date_diff = RelativeDeltaField()
    cost_per_word = MoneyField(max_digits=5,
                               decimal_places=4,
                               default=Money(0, 'USD'),
                               default_currency='USD')


class DefaultTranslationEstTemplate(models.Model):
    date_diff = RelativeDeltaField()
    cost_per_word = MoneyField(max_digits=5,
                               decimal_places=4,
                               default=Money(0, 'USD'),
                               default_currency='USD')


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

    def save(self, **kwargs):
        # official_cost
        self.law_firm_cost = convert_money(self.law_firm_cost, 'USD')
        super().save(kwargs)


class BaseEst(models.Model):
    official_cost = MoneyField(max_digits=19,
                               decimal_places=4,
                               default=Money(0, 'USD'),
                               default_currency='USD')
    date = models.DateField()
    law_firm_est = models.OneToOneField(LawFirmEst, on_delete=models.CASCADE, null=True)
    application = models.ForeignKey(BaseApplication,
                                    on_delete=models.CASCADE)
    translation_bool = models.BooleanField(default=False)

    objects = EstimateManager()
    class Meta:
        abstract = False

    def save(self, **kwargs):
        # official_cost
        self.official_cost = convert_money(self.official_cost, 'USD')
        super().save(kwargs)


class FilingEstimate(BaseEst):
    
    class Meta:
        abstract = False


class OAEstimate(BaseEst):
    office_action = models.ForeignKey(OfficeAction,
                                      on_delete=models.CASCADE)

    objects = OAEstimateManager()
    class Meta:
        abstract = False

class USOAEstimate(BaseEst):
    office_action = models.ForeignKey(USOfficeAction,
                                      on_delete=models.CASCADE)
    objects = USOAEstimateManager()

class PublicationEst(BaseEst):
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE)

    objects = PublEstimateManager()
    class Meta:
        abstract = False


class AllowanceEst(BaseEst):
    allowance = models.ForeignKey(Allowance, on_delete=models.CASCADE)

    objects = AllowanceEstimateManager()

    class Meta:
        abstract = False


class IssueEst(BaseEst):
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)

    objects = IssueEstimateManager()

    class Meta:
        abstract = False

# class TranslationEst(BaseEst):
#
#     class Meta:
#         abstract = False
