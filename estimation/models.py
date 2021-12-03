import math

from dateutil.relativedelta import relativedelta
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
from application.models.requestExamination import RequestExamination
from application.models.usOfficeAction import USOfficeAction
from application.models.utilityApplication import UtilityApplication
from characteristics.enums import ApplTypes
from characteristics.models import Country, EntitySize, ApplType, Language, DocFormat
from estimation.managers import EstimateManager, OAEstimateManager, USOAEstimateManager, PublEstimateManager, \
    AllowanceEstimateManager, IssueEstimateManager, ReqExamEstimateManager
from application import utils as applUtils


class FeeCategory(models.Model):
    name = models.CharField(max_length=200)


class ComplexTimeConditions(models.Model):
    name = models.CharField(max_length=200)

    def calc_complex_time_condition(self, application, date_diff, template_conditions):
        if (self.name == 'from priority date'):
            return self.calc_from_priority_date(application, date_diff)
        elif (self.name == 'from ep filing date'):
            return self.calc_from_date_of_parent_ep_application(application, date_diff)
        elif (self.name == 'from date of parent ep appl acc fees'):
            return self.calc_from_date_of_parent_ep_appl_acc_fees(application, date_diff)
        elif (self.name == 'from date of filing and issue acc fees'):
            return self.calc_acc_fees_from_filing_to_issue(application, date_diff)
        elif (self.name == 'from inter filing date or filing date'):
            return self.calc_from_international_filing_date_or_filing_date()
        # elif (self.name == 'from 4th anniversary of filing date until grant'):
        #     return self.calc_from_4th_anniversary_of_filing_date_until_grant()
        return None

    # def calc_from_4th_anniversary_of_filing_date_until_grant(self, application, date_diff):
    #     # use applOption to retrieve allowance_option
    #     appl_option = application.appl_option
    #
    #     # sum Delta Time between filing and allowance_option
    #     delta_t = relativedelta(days=0)
    #
    #     if (IssueOptions.objects.filter(appl=appl_option).exists()):
    #         allow_option = IssueOptions.objects.get(appl=appl_option)
    #         delta_t += allow_option.date_diff
    #     if (AllowOptions.objects.filter(appl=appl_option).exists()):
    #         allow_option = AllowOptions.objects.get(appl=appl_option)
    #         delta_t += allow_option.date_diff
    #
    #     if (OAOptions.objects.filter(appl=appl_option).exists()):
    #         oa_options = OAOptions.objects.filter(appl=appl_option)
    #         for oa in oa_options:
    #             delta_t += oa.date_diff
    #
    #
    #     # templates = templates.exclude(
    #     #     Q(conditions__condition_annual_prosecution_fee=True)
    #     #     & Q(date_diff__gt=delta_t))
    #     # return templates

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
        if prior_application:
            if (applUtils.convert_class_applType(prior_application).get_enum()
                    is ApplTypes.EP):
                new_date = prior_application.date_filing + date_diff

        return new_date

    def calc_from_date_of_parent_ep_appl_acc_fees(self, application, date_diff):
        # date of EP and date of EP validation
        # accumulate any values that happen between date of EP and EPValidation
        # implement the date on the date of filing the EPValidation
        # otherwise implement date_diff from ep filing date
        new_date = application.date_filing + date_diff
        prior_application = application.prior_appl
        if prior_application:
            if (applUtils.convert_class_applType(prior_application).get_enum()
                    is ApplTypes.EP):
                new_date = prior_application.date_filing + date_diff
                if new_date < application.date_filing:
                    new_date = application.date_filing

        return new_date

    def calc_acc_fees_from_filing_to_issue(self, application, date_diff):
        # date of filing and date of issuance
        # accumulate any values that happen between date of filing and issuance
        # implement the date on the date of issuance
        # otherwise implement date_diff from filing date
        new_date = application.date_filing + date_diff
        issue = application.issue
        if issue:
            if (applUtils.convert_class_applType(issue).get_enum()
                    is ApplTypes.EP):
                new_date = application.date_filing + date_diff
                if new_date < issue.date_issuance:
                    new_date = issue.date_issueance

        return new_date

    def calc_from_international_filing_date_or_filing_date(self, application, date_diff):
        # from date of international filing
        # from pct phase
        new_date = application.date_filing + date_diff
        prior_application = application.prior_appl
        if prior_application:
            new_date = prior_application.date_filing + date_diff

        return new_date


class ComplexConditions(models.Model):
    name = models.CharField(max_length=200)

    def calc_complex_condition(self, appl_details, cost, template_conditions):
        if self.name == 'multiply each by template above minimum indep claims':
            return self.calc_multiply_each_by_template_above_minimum_indep_claims(appl_details,
                                                                                  template_conditions,
                                                                                  cost)
        elif self.name == 'multiply each by template above minimum total claims':
            return self.calc_multiply_each_by_template_above_minimum_total_claims(appl_details,
                                                                                  template_conditions,
                                                                                  cost)
        elif self.name == 'calc multiply each above min multiple dependent claims':
            return self.calc_multiply_each_above_min_multiple_dependent_claim(appl_details,
                                                                              template_conditions,
                                                                              cost)
        elif self.name == 'multiply each by template above minimum claims by unit of 5 claims':
            return self.calc_multiply_each_by_template_above_minimum_claims_by_unit_of_5_claims(appl_details,
                                                                                                template_conditions,
                                                                                                cost)
        elif self.name == 'multiply each page by unit of fifty pages':
            return self.calc_multiply_each_by_template_above_minimum_total_claims(appl_details,
                                                                                  template_conditions,
                                                                                  cost)
        elif self.name == 'multiply each addl page':
            return self.calc_multiply_each_additional_page(appl_details,
                                                           template_conditions,
                                                           cost)
        elif self.name == 'date_diff from earliest priority_date':
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
        if template_conditions.condition_indep_claims_min:
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
        if template_conditions.condition_claims_min:
            num_fee_claims = appl_details.num_claims - template_conditions.condition_claims_min
        else:
            num_fee_claims = appl_details.num_claims
        fee = num_fee_claims * cost
        return fee

    def calc_multiply_each_above_min_multiple_dependent_claim(self, appl_details,
                                                              template_conditions,
                                                              cost):
        # $100 per claim in excess of 20
        # 21 claims will yield a fee of $100
        if template_conditions.condition_claims_multiple_dependent_min:
            num_fee_claims = appl_details.num_claims_multiple_dependent - template_conditions.condition_claims_multiple_dependent_min
        else:
            num_fee_claims = appl_details.num_claims_multiple_dependent
        fee = num_fee_claims * cost
        return fee

    def calc_multiply_each_by_template_above_minimum_claims_by_unit_of_5_claims(self, appl_details,
                                                                                template_conditions,
                                                                                cost):
        # $120 per 5th claim in excess of 25
        # 31 claims will yield a fee of $120
        # 34 claims will yield a fee of $120
        # 43 claims will yield a fee of $360
        if template_conditions.condition_claims_min:
            num_fee = math.floor(appl_details.num_claims - template_conditions.condition_claims_min) / 5
        else:
            num_fee = math.floor(appl_details.num_claims) / 5
        fee = num_fee * cost
        return fee

    def calc_multiply_each_page_by_unit_of_fifty_pages(self, appl_details,
                                                       template_conditions,
                                                       cost):
        # $100 per set of 50 pages in excess of 100
        # 150 pages will yield a fee of $100
        if template_conditions.condition_pages_min:
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
        if template_conditions.condition_pages_min:
            total_pages = appl_details.total_pages - template_conditions.condition_pages_min
        else:
            total_pages = appl_details.total_pages - 0
        fee = total_pages * cost
        return fee


class LineEstimationTemplateConditions(models.Model):
    # claims
    condition_claims_multiple_dependent_min = models.IntegerField(blank=True, null=True)
    condition_claims_multiple_dependent_max = models.IntegerField(blank=True, null=True)
    condition_claims_min = models.IntegerField(blank=True, null=True)
    condition_claims_max = models.IntegerField(blank=True, null=True)
    condition_indep_claims_min = models.IntegerField(blank=True, null=True)
    condition_indep_claims_max = models.IntegerField(blank=True, null=True)

    # pages
    condition_pages_total_min = models.IntegerField(blank=True, null=True)
    condition_pages_total_max = models.IntegerField(blank=True, null=True)
    condition_pages_desc_min = models.IntegerField(blank=True, null=True)
    condition_pages_desc_max = models.IntegerField(blank=True, null=True)
    condition_pages_claims_min = models.IntegerField(blank=True, null=True)
    condition_pages_claims_max = models.IntegerField(blank=True, null=True)
    condition_pages_drawings_min = models.IntegerField(blank=True, null=True)
    condition_pages_drawings_max = models.IntegerField(blank=True, null=True)

    condition_drawings_min = models.IntegerField(blank=True, null=True)
    condition_drawings_max = models.IntegerField(blank=True, null=True)
    condition_entity_size = models.ForeignKey(EntitySize,
                                              on_delete=models.CASCADE,
                                              null=True)
    condition_annual_prosecution_fee = models.BooleanField(default=False)
    condition_annual_prosecution_fee_until_grant = models.BooleanField(default=False)
    condition_renewal_fee_from_filing_after_grant = models.BooleanField(default=False)
    condition_complex = models.ForeignKey(ComplexConditions,
                                          on_delete=models.CASCADE,
                                          null=True, default=None)
    condition_time_complex = models.ForeignKey(ComplexTimeConditions,
                                               on_delete=models.CASCADE,
                                               null=True, default=None)
    prior_pct = models.BooleanField(null=True)
    prior_pct_same_country = models.BooleanField(null=True)
    prev_appl_date_excl_intermediary_time = models.BooleanField(default=False)
    prior_appl_exists = models.BooleanField(default=None, null=True)
    doc_format = models.ForeignKey(DocFormat, default=None, null=True, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, default=None, null=True, on_delete=models.CASCADE)


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
    isa_country_fee_only = models.BooleanField(default=False)
    law_firm_template = models.OneToOneField(LawFirmEstTemplate, on_delete=models.CASCADE)
    description = models.TextField()
    fee_code = models.CharField(max_length=30)
    fee_category = models.ForeignKey(FeeCategory, on_delete=models.CASCADE)

    # objects = TemplateManager()

    class Meta:
        abstract = True

    # def save(self, *args, **kwargs):
    #     # override so the country and currency are correct
    #     self.official_cost = Money(self.official_cost.amount, self.country.currency_name)
    #     self.law_firm_template.law_firm_cost = \
    #         Money(self.law_firm_template.law_firm_cost.amount, self.country.currency_name)
    #     self.law_firm_template.save()
    #     return super().save()


class FilingEstimateTemplate(BaseEstTemplate):
    class Meta:
        abstract = False


class PublicationEstTemplate(BaseEstTemplate):
    class Meta:
        abstract = False


class RequestExamEstTemplate(BaseEstTemplate):
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
    start_language = models.ForeignKey(Language, on_delete=models.CASCADE, related_name='start_language_est_temp')
    end_language = models.ForeignKey(Language, on_delete=models.CASCADE, related_name='end_language_est_temp')
    date_diff = RelativeDeltaField()
    cost_per_word = MoneyField(max_digits=19,
                               decimal_places=4,
                               default=Money(0, 'USD'),
                               default_currency='USD')


class DefaultTranslationEstTemplate(models.Model):
    date_diff = RelativeDeltaField()
    cost_per_word = MoneyField(max_digits=19,
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
        self.law_firm_cost = convert_money(self.law_firm_cost, 'USD')
        super().save(kwargs)


class BaseEst(models.Model):
    official_cost = MoneyField(max_digits=19,
                               decimal_places=4,
                               default=Money(0, 'USD'),
                               default_currency='USD')
    date = models.DateField()
    description = models.TextField()
    fee_code = models.CharField(max_length=30)
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


class RequestExamEst(BaseEst):
    exam_request = models.ForeignKey(RequestExamination, on_delete=models.CASCADE)

    objects = ReqExamEstimateManager()

    class Meta:
        abstract = False


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
