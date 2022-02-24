import math

from django.db import models
from djmoney.contrib.exchange.models import convert_money
from djmoney.models.fields import MoneyField
from djmoney.money import Money
from relativedeltafield import RelativeDeltaField
from characteristics.enums import ApplTypes
from characteristics.models import Country, DetailedFeeCategory, EntitySize, ApplType, Language, DocFormat, FeeCategory
from estimation.managers import EstimateManager, OAEstimateManager, USOAEstimateManager, PublEstimateManager, \
    AllowanceEstimateManager, IssueEstimateManager, ReqExamEstimateManager
from application import utils as applUtils
from famform.models import ApplOptions


class ComplexTimeConditions(models.Model):
    name = models.CharField(max_length=200)

    def calc_complex_time_condition(self, application, date_diff, template_conditions):
        if self.name == 'from priority date':
            return self.calc_from_priority_date(application, date_diff)
        elif self.name == 'from ep filing date':
            return self.calc_from_date_of_parent_ep_application(application, date_diff)
        elif self.name == 'from date of parent ep appl acc fees':
            return self.calc_from_date_of_parent_ep_appl_acc_fees(application, date_diff)
        elif self.name == 'from date of filing and issue acc fees':
            return self.calc_acc_fees_from_filing_to_issue(application, date_diff)
        elif self.name == 'from inter filing date or filing date':
            return self.calc_from_international_filing_date_or_filing_date(application, date_diff)
        elif self.name == 'from filing date':
            return self.calc_from_filing_date(application, date_diff)
        return None

    def calc_from_filing_date(self, application, date_diff):
        return application.date_filing + date_diff

    def calc_from_priority_date(self, application, date_diff):
        appl = application
        new_date = application.date_filing + date_diff
        while appl != None:
            prior_appl = appl.prior_appl
            if prior_appl == None:
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
            new_date = application.date_filing + date_diff
            if new_date < issue.date_issuance:
                new_date = issue.date_issuance

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

    def calc_complex_condition(self, application, cost, template_conditions):
        appl_details = application.details

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
        elif self.name == 'multiply each page by unit of zero to fifty pages':
            return self.calc_multiply_each_page_by_unit_of_zero_to_fifty_pages(appl_details,
                                                                               template_conditions,
                                                                               cost)
        elif self.name == 'multiply each page by unit of fifteen pages':
            return self.calc_multiply_each_page_by_unit_of_fifteen_pages(appl_details,
                                                                         template_conditions,
                                                                         cost)
        elif self.name == 'multiply each addl page':
            return self.calc_multiply_each_additional_page(appl_details,
                                                           template_conditions,
                                                           cost)

        elif self.name == 'calc fee per each child country max fee at seven':
            return self.calc_fee_per_each_child_country_max_fee_at_seven(application=application, cost=cost)

        elif self.name == 'calc fee per each 5 claims':
            return self.calc_fee_per_each_five_claims(appl_details=appl_details,
                                                      template_conditions=template_conditions,
                                                      cost=cost)
        elif self.name == 'calc fee per each 10 claims':
            return self.calc_fee_per_each_ten_claims(appl_details=appl_details,
                                                     template_conditions=template_conditions,
                                                     cost=cost)
        elif self.name == 'calc fee per 4 pages or fraction of 4 pages of parent application':
            return self.calc_fee_per_4_pages_or_fraction_of_four_pages_of_parent_application(
                application=application, template_conditions=template_conditions, cost=cost
            )

        return None

    def calc_fee_per_4_pages_or_fraction_of_four_pages_of_parent_application(self, application,
                                                                             template_conditions,
                                                                             cost):

        fee = Money(0, cost.currency)
        if application.prior_appl:
            fee = cost * math.ceil(application.prior_appl.details.total_pages / 4)
        return fee

    def calc_fee_per_each_ten_claims(self, appl_details,
                                     template_conditions,
                                     cost):
        fee = Money(0, cost.currency)
        condition_min = template_conditions.condition_claims_min
        condition_max = template_conditions.condition_claims_max
        if condition_min:
            num_fee_claims = appl_details.num_claims - condition_min
        else:
            num_fee_claims = appl_details.num_claims

        if condition_max:
            min_max_diff = condition_max
            if condition_min:
                min_max_diff = condition_max - condition_min
            num_fee_claims = min(min_max_diff, num_fee_claims)
        if num_fee_claims > 0:
            fee = int(num_fee_claims / 10) * cost
        return fee

    def calc_fee_per_each_five_claims(self, appl_details,
                                      template_conditions,
                                      cost):
        fee = Money(0, cost.currency)
        condition_min = template_conditions.condition_claims_min
        condition_max = template_conditions.condition_claims_max
        if condition_min:
            num_fee_claims = appl_details.num_claims - condition_min
        else:
            num_fee_claims = appl_details.num_claims

        if condition_max:
            min_max_diff = condition_max
            if condition_min:
                min_max_diff = condition_max - condition_min
            num_fee_claims = min(min_max_diff, num_fee_claims)
        if num_fee_claims > 0:
            fee = int(num_fee_claims / 5) * cost
        return fee

    def calc_fee_per_each_child_country_max_fee_at_seven(self, application, cost):
        # determine the number of child applications
        # need appl_options
        appl_option = application.appl_option
        # find child_options
        num_child_appl_options = ApplOptions.objects.filter(prev_appl_options=appl_option).count()
        # multiply number of child options by cost
        if num_child_appl_options < 7:
            tot_cost = num_child_appl_options * cost
        else:
            tot_cost = num_child_appl_options * 7

        return tot_cost

    def calc_multiply_each_by_template_above_minimum_indep_claims(self, appl_details,
                                                                  template_conditions,
                                                                  cost):
        # $100 per indep claim in excess of 3
        # 5 claims will yield a fee of $200
        # 7 claims will yield a fee of $400
        # and stops calculation at max
        fee = Money(0, cost.currency)
        condition_min = template_conditions.condition_indep_claims_min
        condition_max = template_conditions.condition_indep_claims_max
        if condition_min:
            num_fee_claims = appl_details.num_indep_claims - condition_min
        else:
            num_fee_claims = appl_details.num_indep_claims

        if condition_max:
            min_max_diff = condition_max
            if condition_min:
                min_max_diff = condition_max - condition_min
            num_fee_claims = min(min_max_diff, num_fee_claims)
        if num_fee_claims > 0:
            fee = num_fee_claims * cost
        return fee

    def calc_multiply_each_by_template_above_minimum_total_claims(self, appl_details,
                                                                  template_conditions,
                                                                  cost):
        # $100 per claim in excess of 20
        # 21 claims will yield a fee of $100
        fee = Money(0, cost.currency)
        condition_min = template_conditions.condition_claims_min
        condition_max = template_conditions.condition_claims_max
        if condition_min:
            num_fee_claims = appl_details.num_claims - condition_min
        else:
            num_fee_claims = appl_details.num_claims

        if condition_max:
            min_max_diff = condition_max
            if condition_min:
                min_max_diff = condition_max - condition_min
            num_fee_claims = min(min_max_diff, num_fee_claims)
        if num_fee_claims > 0:
            fee = num_fee_claims * cost
        return fee

    def calc_multiply_each_above_min_multiple_dependent_claim(self, appl_details,
                                                              template_conditions,
                                                              cost):
        # $100 per claim in excess of 20
        # 21 claims will yield a fee of $100
        fee = Money(0, cost.currency)
        condition_min = template_conditions.condition_claims_multiple_dependent_min
        condition_max = template_conditions.condition_claims_multiple_dependent_max
        if condition_min:
            num_fee_claims = appl_details.num_claims_multiple_dependent - condition_min
        else:
            num_fee_claims = appl_details.num_claims_multiple_dependent

        if condition_max:
            min_max_diff = condition_max
            if condition_min:
                min_max_diff = condition_max - condition_min
            num_fee_claims = min(min_max_diff, num_fee_claims)
        if num_fee_claims > 0:
            fee = num_fee_claims * cost
        return fee

    def calc_multiply_each_by_template_above_minimum_claims_by_unit_of_5_claims(self, appl_details,
                                                                                template_conditions,
                                                                                cost):
        # $120 per 5th claim in excess of 25
        # 31 claims will yield a fee of $120
        # 34 claims will yield a fee of $120
        # 43 claims will yield a fee of $360
        fee = Money(0, cost.currency)
        condition_min = template_conditions.condition_claims_min
        condition_max = template_conditions.condition_claims_max
        if condition_min:
            num_fee = math.floor((appl_details.num_claims - template_conditions.condition_claims_min) / 5)
            # num_fee_claims = appl_details.num_claims - condition_min
        else:
            num_fee = math.floor(appl_details.num_claims / 5)
            # num_fee_claims = appl_details.num_claims

        if condition_max:
            min_max_diff = math.floor(condition_max / 5)
            if condition_min:
                min_max_diff = math.floor((condition_max - condition_min) / 5)
            # num_fee_claims = min(min_max_diff, num_fee_claims)
            num_fee = min(min_max_diff, num_fee)
        if num_fee > 0:
            fee = num_fee * cost
        return fee

    def calc_multiply_each_page_by_unit_of_fifteen_pages(self, appl_details,
                                                         template_conditions,
                                                         cost):
        # $100 per set of 50 pages in excess of 100
        # 150 pages will yield a fee of $100
        fee = Money(0, cost.currency)
        condition_min = template_conditions.condition_pages_total_min
        condition_max = template_conditions.condition_pages_total_max
        if condition_min:
            num_fee = math.floor((appl_details.total_pages - template_conditions.condition_pages_total_min) / 15)
            # num_fee_claims = appl_details.num_claims - condition_min
        else:
            num_fee = math.floor(appl_details.total_pages / 15)
            # num_fee_claims = appl_details.num_claims

        if condition_max:
            min_max_diff = math.floor(condition_max / 15)
            if condition_min:
                min_max_diff = math.floor((condition_max - condition_min) / 15)
            # num_fee_claims = min(min_max_diff, num_fee_claims)
            num_fee = min(min_max_diff, num_fee)
        if num_fee > 0:
            fee = num_fee * cost
        return fee

    def calc_multiply_each_page_by_unit_of_fifty_pages(self, appl_details,
                                                       template_conditions,
                                                       cost):
        # $100 per set of 50 pages in excess of 100
        # 150 pages will yield a fee of $100
        fee = Money(0, cost.currency)
        condition_min = template_conditions.condition_pages_total_min
        condition_max = template_conditions.condition_pages_total_max
        if condition_min:
            num_fee = math.floor((appl_details.total_pages - template_conditions.condition_pages_total_min) / 50)
            # num_fee_claims = appl_details.num_claims - condition_min
        else:
            num_fee = math.floor(appl_details.total_pages / 50)
            # num_fee_claims = appl_details.num_claims

        if condition_max:
            min_max_diff = math.floor(condition_max / 50)
            if condition_min:
                min_max_diff = math.floor((condition_max - condition_min) / 50)
            # num_fee_claims = min(min_max_diff, num_fee_claims)
            num_fee = min(min_max_diff, num_fee)
        if num_fee > 0:
            fee = num_fee * cost
        return fee

    def calc_multiply_each_page_by_unit_of_zero_to_fifty_pages(self, appl_details,
                                                               template_conditions,
                                                               cost):
        # $100 per set of 50 pages in excess of 100
        # 150 pages will yield a fee of $100
        fee = Money(0, cost.currency)
        condition_min = template_conditions.condition_pages_total_min
        condition_max = template_conditions.condition_pages_total_max
        if condition_min:
            num_fee = math.ceil((appl_details.total_pages - template_conditions.condition_pages_total_min) / 50)
            # num_fee_claims = appl_details.num_claims - condition_min
        else:
            num_fee = math.ceil(appl_details.total_pages / 50)
            # num_fee_claims = appl_details.num_claims

        if condition_max:
            min_max_diff = math.ceil(condition_max / 50)
            if condition_min:
                min_max_diff = math.ceil((condition_max - condition_min) / 50)
            # num_fee_claims = min(min_max_diff, num_fee_claims)
            num_fee = min(min_max_diff, num_fee)
        if num_fee > 0:
            fee = num_fee * cost
        return fee

    def calc_multiply_each_additional_page(self, appl_details,
                                           template_conditions,
                                           cost):
        # $100 per set of 50 pages in excess of 100
        # 150 pages will yield a fee of $100
        fee = Money(0, cost.currency)
        condition_min = template_conditions.condition_pages_total_min
        condition_max = template_conditions.condition_pages_total_max
        if condition_min:
            num_fee_claims = appl_details.total_pages - condition_min
        else:
            num_fee_claims = appl_details.total_pages

        if condition_max:
            min_max_diff = condition_max
            if condition_min:
                min_max_diff = condition_max - condition_min
            num_fee_claims = min(min_max_diff, num_fee_claims)
        if num_fee_claims > 0:
            fee = num_fee_claims * cost
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
    condition_renewal_fee_from_filing_of_prior_after_grant = models.BooleanField(default=False)
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
    isa_country_fee_only = models.BooleanField(default=False)
    doc_format = models.ForeignKey(DocFormat, default=None, null=True, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, default=None, null=True, on_delete=models.CASCADE)


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
    country = models.ForeignKey(Country, on_delete=models.PROTECT)
    appl_type = models.ForeignKey(ApplType, on_delete=models.PROTECT)

    conditions = models.OneToOneField(LineEstimationTemplateConditions, on_delete=models.PROTECT)
    law_firm_template = models.OneToOneField(LawFirmEstTemplate, on_delete=models.PROTECT)
    description = models.TextField()
    fee_code = models.CharField(max_length=30)
    fee_category = models.ForeignKey(FeeCategory, on_delete=models.PROTECT)
    detailed_fee_category = models.ForeignKey(DetailedFeeCategory, on_delete=models.PROTECT)

    class Meta:
        abstract = True


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
    law_firm_est = models.OneToOneField('LawFirmEst', on_delete=models.CASCADE, null=True)
    application = models.ForeignKey('application.BaseApplication',
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
    office_action = models.ForeignKey('application.OfficeAction',
                                      on_delete=models.CASCADE)

    objects = OAEstimateManager()

    class Meta:
        abstract = False


class USOAEstimate(BaseEst):
    office_action = models.ForeignKey('application.USOfficeAction',
                                      on_delete=models.CASCADE)
    objects = USOAEstimateManager()


class RequestExamEst(BaseEst):
    exam_request = models.ForeignKey('application.RequestExamination', on_delete=models.CASCADE)

    objects = ReqExamEstimateManager()

    class Meta:
        abstract = False


class PublicationEst(BaseEst):
    publication = models.ForeignKey('application.Publication', on_delete=models.CASCADE)

    objects = PublEstimateManager()

    class Meta:
        abstract = False


class AllowanceEst(BaseEst):
    allowance = models.ForeignKey('application.Allowance', on_delete=models.CASCADE)

    objects = AllowanceEstimateManager()

    class Meta:
        abstract = False


class IssueEst(BaseEst):
    issue = models.ForeignKey('application.Issue', on_delete=models.CASCADE)

    objects = IssueEstimateManager()

    class Meta:
        abstract = False
