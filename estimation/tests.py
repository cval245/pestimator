from datetime import date

from dateutil.relativedelta import relativedelta
from django.test import TestCase
from djmoney.money import Money

from application.factories import AllowanceFactory, ApplDetailsFactory, BaseUtilityApplicationFactory, \
    EPApplicationFactory, IssuanceFactory, \
    OfficeActionFactory, PCTApplicationFactory, PublicationFactory, RequestExaminationFactory
from characteristics.factories import ApplTypeFactory, CountryFactory, DocFormatFactory, EntitySizeFactory, \
    LanguageFactory
from famform.factories import AllowOptionsFactory, ApplOptionsFactory, ApplOptionsParticularsFactory, \
    IssueOptionsFactory, OAOptionsFactory, \
    PublOptionFactory, RequestExaminationOptionFactory
from . import factories
from . import utils
from .factories import ComplexConditionsFactory, ComplexTimeConditionsFactory
from .models import FilingEstimateTemplate, LineEstimationTemplateConditions


class ComplexTimeConditionsTest(TestCase):

    def test_calc_from_priority_date_with_one_priority_appl(self):
        prior_application = BaseUtilityApplicationFactory(prior_appl=None, date_filing=date(2023, 5, 8))
        application = BaseUtilityApplicationFactory(prior_appl=prior_application, date_filing=date(2024, 4, 3))
        cmplxTimeConds = ComplexTimeConditionsFactory()
        new_date = cmplxTimeConds.calc_from_priority_date(application=application,
                                                          date_diff=relativedelta(months=16))
        self.assertEquals(new_date, date(2024, 9, 8))

    def test_calc_from_priority_date_with_two_priority_appl(self):
        prior_application_1 = BaseUtilityApplicationFactory(prior_appl=None, date_filing=date(2020, 2, 4))
        prior_application = BaseUtilityApplicationFactory(prior_appl=prior_application_1, date_filing=date(2023, 5, 8))
        application = BaseUtilityApplicationFactory(prior_appl=prior_application, date_filing=date(2024, 4, 3))
        cmplxTimeConds = ComplexTimeConditionsFactory()
        new_date = cmplxTimeConds.calc_from_priority_date(application=application,
                                                          date_diff=relativedelta(months=16))
        self.assertEquals(new_date, date(2021, 6, 4))

    def test_calc_from_priority_date_with_no_priority_appl(self):
        application = BaseUtilityApplicationFactory(prior_appl=None, date_filing=date(2024, 4, 3))
        cmplxTimeConds = ComplexTimeConditionsFactory()
        new_date = cmplxTimeConds.calc_from_priority_date(application=application,
                                                          date_diff=relativedelta(months=16))
        self.assertEquals(new_date, date(2025, 8, 3))

    def test_calc_from_date_of_parent_ep_application_parent_is_ep(self):
        appl_type_ep = ApplTypeFactory(ep=True)
        prior_application_1 = BaseUtilityApplicationFactory(prior_appl=None, date_filing=date(2020, 2, 4))
        prior_application = EPApplicationFactory(prior_appl=prior_application_1, date_filing=date(2023, 5, 8))
        application = BaseUtilityApplicationFactory(prior_appl=prior_application, date_filing=date(2024, 4, 3))
        cmplxTimeConds = ComplexTimeConditionsFactory()
        new_date = cmplxTimeConds.calc_from_date_of_parent_ep_application(application=application,
                                                                          date_diff=relativedelta(months=16))
        self.assertEquals(new_date, date(2024, 9, 8))

    def test_calc_from_date_of_parent_ep_application_but_no_ep_application(self):
        appl_type_ep = ApplTypeFactory(ep=True)
        prior_application_1 = BaseUtilityApplicationFactory(prior_appl=None, date_filing=date(2020, 2, 4))
        prior_application = BaseUtilityApplicationFactory(prior_appl=prior_application_1, date_filing=date(2023, 5, 8))
        application = BaseUtilityApplicationFactory(prior_appl=prior_application, date_filing=date(2024, 4, 3))
        cmplxTimeConds = ComplexTimeConditionsFactory()
        new_date = cmplxTimeConds.calc_from_date_of_parent_ep_application(application=application,
                                                                          date_diff=relativedelta(months=16))
        self.assertEquals(new_date, date(2025, 8, 3))

    def test_calc_from_date_of_parent_ep_appl_acc_fees_accumulating(self):
        appl_type_ep = ApplTypeFactory(ep=True)
        prior_application_1 = BaseUtilityApplicationFactory(prior_appl=None, date_filing=date(2020, 2, 4))
        prior_application = EPApplicationFactory(prior_appl=prior_application_1, date_filing=date(2023, 5, 8))
        application = BaseUtilityApplicationFactory(prior_appl=prior_application, date_filing=date(2024, 4, 3))
        cmplxTimeConds = ComplexTimeConditionsFactory()
        new_date = cmplxTimeConds.calc_from_date_of_parent_ep_appl_acc_fees(application=application,
                                                                            date_diff=relativedelta(months=3))
        self.assertEquals(new_date, date(2024, 4, 3))

    def test_calc_from_date_of_parent_ep_appl_acc_fees_beyond_accumulating(self):
        appl_type_ep = ApplTypeFactory(ep=True)
        prior_application_1 = BaseUtilityApplicationFactory(prior_appl=None, date_filing=date(2020, 2, 4))
        prior_application = EPApplicationFactory(prior_appl=prior_application_1, date_filing=date(2023, 5, 8))
        application = BaseUtilityApplicationFactory(prior_appl=prior_application, date_filing=date(2024, 4, 3))
        cmplxTimeConds = ComplexTimeConditionsFactory()
        new_date = cmplxTimeConds.calc_from_date_of_parent_ep_appl_acc_fees(application=application,
                                                                            date_diff=relativedelta(months=16))
        self.assertEquals(new_date, date(2024, 9, 8))

    def test_calc_acc_fees_from_filing_to_issue_accumulating(self):
        application = BaseUtilityApplicationFactory(prior_appl=None, date_filing=date(2024, 4, 3))
        issue = IssuanceFactory(application=application, date_issuance=date(2028, 2, 5))
        cmplxTimeConds = ComplexTimeConditionsFactory()
        new_date = cmplxTimeConds.calc_acc_fees_from_filing_to_issue(application=application,
                                                                     date_diff=relativedelta(months=6))
        self.assertEquals(new_date, date(2028, 2, 5))

    def test_calc_acc_fees_from_filing_to_issue_beyond_accumulating(self):
        application = BaseUtilityApplicationFactory(prior_appl=None, date_filing=date(2024, 4, 3))
        issue = IssuanceFactory(application=application, date_issuance=date(2028, 2, 5))
        cmplxTimeConds = ComplexTimeConditionsFactory()
        new_date = cmplxTimeConds.calc_acc_fees_from_filing_to_issue(application=application,
                                                                     date_diff=relativedelta(years=6))
        self.assertEquals(new_date, date(2030, 4, 3))

    def test_calc_from_international_filing_date_of_filing_date_one_priority(self):
        prior_application = PCTApplicationFactory(prior_appl=None, date_filing=date(2023, 5, 8))
        application = BaseUtilityApplicationFactory(prior_appl=prior_application, date_filing=date(2024, 4, 3))
        cmplxTimeConds = ComplexTimeConditionsFactory()
        new_date = cmplxTimeConds.calc_from_international_filing_date_or_filing_date(application=application,
                                                                                     date_diff=relativedelta(months=16))
        self.assertEquals(new_date, date(2024, 9, 8))

    def test_calc_from_international_filing_date_of_filing_date_two_priority(self):
        prior_application_1 = BaseUtilityApplicationFactory(prior_appl=None, date_filing=date(2020, 2, 4))
        prior_application = PCTApplicationFactory(prior_appl=prior_application_1, date_filing=date(2023, 5, 8))
        application = BaseUtilityApplicationFactory(prior_appl=prior_application, date_filing=date(2024, 4, 3))
        cmplxTimeConds = ComplexTimeConditionsFactory()
        new_date = cmplxTimeConds.calc_from_international_filing_date_or_filing_date(application=application,
                                                                                     date_diff=relativedelta(months=16))
        self.assertEquals(new_date, date(2024, 9, 8))

    def test_calc_from_international_filing_date_of_filing_date_no_priority(self):
        application = BaseUtilityApplicationFactory(prior_appl=None, date_filing=date(2024, 4, 3))
        cmplxTimeConds = ComplexTimeConditionsFactory()
        new_date = cmplxTimeConds.calc_from_international_filing_date_or_filing_date(application=application,
                                                                                     date_diff=relativedelta(months=16))
        self.assertEquals(new_date, date(2025, 8, 3))


class ComplexConditionsTest(TestCase):

    def test_calc_multiple_each_by_template_above_minimum_indep_claims_returns_zero(self):
        details = ApplDetailsFactory(num_indep_claims=5)
        conditions = LineEstimationTemplateConditions(condition_indep_claims_min=10)
        cmplxConds = ComplexConditionsFactory()
        cost = Money(100, 'USD')
        fee = cmplxConds.calc_multiply_each_by_template_above_minimum_indep_claims(
            appl_details=details, template_conditions=conditions, cost=cost)
        self.assertEquals(fee.amount, 0)

    def test_calc_multiple_each_by_template_above_minimum_indep_claims(self):
        details = ApplDetailsFactory(num_indep_claims=5)
        conditions = LineEstimationTemplateConditions(condition_indep_claims_min=2)
        cmplxConds = ComplexConditionsFactory()
        cost = Money(100, 'USD')
        fee = cmplxConds.calc_multiply_each_by_template_above_minimum_indep_claims(
            appl_details=details, template_conditions=conditions, cost=cost)
        self.assertEquals(fee.amount, 300)

    def test_calc_multiple_each_by_template_above_minimum_indep_claims_up_to_max(self):
        details = ApplDetailsFactory(num_indep_claims=7)
        conditions = LineEstimationTemplateConditions(condition_indep_claims_min=2, condition_indep_claims_max=5)
        cmplxConds = ComplexConditionsFactory()
        cost = Money(100, 'USD')
        fee = cmplxConds.calc_multiply_each_by_template_above_minimum_indep_claims(
            appl_details=details, template_conditions=conditions, cost=cost)
        self.assertEquals(fee.amount, 300)

    def test_calc_multiply_each_by_template_above_minimum_indep_claims_dependent_no_min(self):
        details = ApplDetailsFactory(num_indep_claims=7)
        conditions = LineEstimationTemplateConditions(condition_indep_claims_max=5)
        cmplxConds = ComplexConditionsFactory()
        cost = Money(100, 'USD')
        fee = cmplxConds.calc_multiply_each_by_template_above_minimum_indep_claims(
            appl_details=details, template_conditions=conditions, cost=cost)
        self.assertEquals(fee.amount, 500)

    def test_calc_multiply_each_by_template_above_minimum_total_claims_returns_zero(self):
        details = ApplDetailsFactory(num_claims=5)
        conditions = LineEstimationTemplateConditions(condition_claims_min=10)
        cmplxConds = ComplexConditionsFactory()
        cost = Money(100, 'USD')
        fee = cmplxConds.calc_multiply_each_by_template_above_minimum_total_claims(
            appl_details=details, template_conditions=conditions, cost=cost)
        self.assertEquals(fee.amount, 0)

    def test_calc_multiply_each_by_template_above_minimum_total_claims(self):
        details = ApplDetailsFactory(num_claims=5)
        conditions = LineEstimationTemplateConditions(condition_claims_min=2)
        cmplxConds = ComplexConditionsFactory()
        cost = Money(100, 'USD')
        fee = cmplxConds.calc_multiply_each_by_template_above_minimum_total_claims(
            appl_details=details, template_conditions=conditions, cost=cost)
        self.assertEquals(fee.amount, 300)

    def test_calc_multiply_each_by_template_above_minimum_total_claims_up_to_max(self):
        details = ApplDetailsFactory(num_claims=7)
        conditions = LineEstimationTemplateConditions(condition_claims_min=2, condition_claims_max=5)
        cmplxConds = ComplexConditionsFactory()
        cost = Money(100, 'USD')
        fee = cmplxConds.calc_multiply_each_by_template_above_minimum_total_claims(
            appl_details=details, template_conditions=conditions, cost=cost)
        self.assertEquals(fee.amount, 300)

    def test_calc_multiply_each_by_template_above_minimum_total_claims_dependent_no_min(self):
        details = ApplDetailsFactory(num_claims=7)
        conditions = LineEstimationTemplateConditions(condition_claims_max=5)
        cmplxConds = ComplexConditionsFactory()
        cost = Money(100, 'USD')
        fee = cmplxConds.calc_multiply_each_by_template_above_minimum_total_claims(
            appl_details=details, template_conditions=conditions, cost=cost)
        self.assertEquals(fee.amount, 500)

    def test_calc_multiply_each_by_template_above_minimum_multiple_dependent_returns_zero(self):
        details = ApplDetailsFactory(num_claims_multiple_dependent=5)
        conditions = LineEstimationTemplateConditions(condition_claims_multiple_dependent_min=10)
        cmplxConds = ComplexConditionsFactory()
        cost = Money(100, 'USD')
        fee = cmplxConds.calc_multiply_each_above_min_multiple_dependent_claim(
            appl_details=details, template_conditions=conditions, cost=cost)
        self.assertEquals(fee.amount, 0)

    def test_calc_multiply_each_by_template_above_minimum_multiple_dependent(self):
        details = ApplDetailsFactory(num_claims_multiple_dependent=5)
        conditions = LineEstimationTemplateConditions(condition_claims_multiple_dependent_min=2)
        cmplxConds = ComplexConditionsFactory()
        cost = Money(100, 'USD')
        fee = cmplxConds.calc_multiply_each_above_min_multiple_dependent_claim(
            appl_details=details, template_conditions=conditions, cost=cost)
        self.assertEquals(fee.amount, 300)

    def test_calc_multiply_each_by_template_above_minimum_multiple_dependent_up_to_max(self):
        details = ApplDetailsFactory(num_claims_multiple_dependent=7)
        conditions = LineEstimationTemplateConditions(condition_claims_multiple_dependent_min=2,
                                                      condition_claims_multiple_dependent_max=5)
        cmplxConds = ComplexConditionsFactory()
        cost = Money(100, 'USD')
        fee = cmplxConds.calc_multiply_each_above_min_multiple_dependent_claim(
            appl_details=details, template_conditions=conditions, cost=cost)
        self.assertEquals(fee.amount, 300)

    def test_calc_multiply_each_by_template_above_minimum_multiple_dependent_no_min(self):
        details = ApplDetailsFactory(num_claims_multiple_dependent=7)
        conditions = LineEstimationTemplateConditions(condition_claims_multiple_dependent_max=5)
        cmplxConds = ComplexConditionsFactory()
        cost = Money(100, 'USD')
        fee = cmplxConds.calc_multiply_each_above_min_multiple_dependent_claim(
            appl_details=details, template_conditions=conditions, cost=cost)
        self.assertEquals(fee.amount, 500)

    def test_calc_multiply_each_additional_page_returns_zero(self):
        details = ApplDetailsFactory(num_pages_drawings=1, num_pages_claims=1, num_pages_description=3)
        conditions = LineEstimationTemplateConditions(condition_pages_total_min=10)
        cmplxConds = ComplexConditionsFactory()
        cost = Money(100, 'USD')
        fee = cmplxConds.calc_multiply_each_additional_page(
            appl_details=details, template_conditions=conditions, cost=cost)
        self.assertEquals(fee.amount, 0)

    def test_calc_multiple_each_additional_page(self):
        details = ApplDetailsFactory(num_pages_drawings=1, num_pages_claims=1, num_pages_description=3)
        conditions = LineEstimationTemplateConditions(condition_pages_total_min=2)
        cmplxConds = ComplexConditionsFactory()
        cost = Money(100, 'USD')
        fee = cmplxConds.calc_multiply_each_additional_page(
            appl_details=details, template_conditions=conditions, cost=cost)
        self.assertEquals(fee.amount, 300)

    def test_calc_multiple_each_additional_page_up_to_max(self):
        details = ApplDetailsFactory(num_pages_drawings=1, num_pages_claims=1, num_pages_description=3)
        conditions = LineEstimationTemplateConditions(condition_pages_total_min=2,
                                                      condition_pages_total_max=5)
        cmplxConds = ComplexConditionsFactory()
        cost = Money(100, 'USD')
        fee = cmplxConds.calc_multiply_each_additional_page(
            appl_details=details, template_conditions=conditions, cost=cost)
        self.assertEquals(fee.amount, 300)

    def test_calc_multiple_each_additional_page_no_min(self):
        details = ApplDetailsFactory(num_pages_drawings=1, num_pages_claims=1, num_pages_description=3)
        conditions = LineEstimationTemplateConditions(condition_pages_total_max=5)
        cmplxConds = ComplexConditionsFactory()
        cost = Money(100, 'USD')
        fee = cmplxConds.calc_multiply_each_additional_page(
            appl_details=details, template_conditions=conditions, cost=cost)
        self.assertEquals(fee.amount, 500)

    def test_calc_multiply_each_by_template_above_minimum_claims_by_unit_of_5_claims_returns_zero_fee(self):
        details = ApplDetailsFactory(num_claims=15)
        conditions = LineEstimationTemplateConditions(condition_claims_min=20)
        cmplxConds = ComplexConditionsFactory()
        cost = Money(100, 'USD')
        fee = cmplxConds.calc_multiply_each_by_template_above_minimum_claims_by_unit_of_5_claims(
            appl_details=details, template_conditions=conditions, cost=cost)
        self.assertEquals(fee.amount, 0)

    def test_calc_multiply_each_by_template_above_minimum_claims_by_unit_of_5_claims_returns_(self):
        details = ApplDetailsFactory(num_claims=25)
        conditions = LineEstimationTemplateConditions(condition_claims_min=20)
        cmplxConds = ComplexConditionsFactory()
        cost = Money(100, 'USD')
        fee = cmplxConds.calc_multiply_each_by_template_above_minimum_claims_by_unit_of_5_claims(
            appl_details=details, template_conditions=conditions, cost=cost)
        self.assertEquals(fee.amount, 100)

    def test_calc_multiply_each_by_template_above_minimum_claims_by_unit_of_5_claims_returns_two(self):
        details = ApplDetailsFactory(num_claims=35)
        conditions = LineEstimationTemplateConditions(condition_claims_min=20, condition_claims_max=30)
        cmplxConds = ComplexConditionsFactory()
        cost = Money(100, 'USD')
        fee = cmplxConds.calc_multiply_each_by_template_above_minimum_claims_by_unit_of_5_claims(
            appl_details=details, template_conditions=conditions, cost=cost)
        self.assertEquals(fee.amount, 200)

    def test_calc_multiply_each_by_template_above_minimum_claims_by_unit_of_5_claims_returns_six(self):
        details = ApplDetailsFactory(num_claims=35)
        conditions = LineEstimationTemplateConditions(condition_claims_max=30)
        cmplxConds = ComplexConditionsFactory()
        cost = Money(100, 'USD')
        fee = cmplxConds.calc_multiply_each_by_template_above_minimum_claims_by_unit_of_5_claims(
            appl_details=details, template_conditions=conditions, cost=cost)
        self.assertEquals(fee.amount, 600)

    def test_calc_multiply_each_page_by_unit_of_fifty_pages_returns_zero_fee(self):
        details = ApplDetailsFactory(num_pages_drawings=1, num_pages_claims=1, num_pages_description=53)
        conditions = LineEstimationTemplateConditions(condition_pages_total_min=20)
        cmplxConds = ComplexConditionsFactory()
        cost = Money(100, 'USD')
        fee = cmplxConds.calc_multiply_each_page_by_unit_of_fifty_pages(
            appl_details=details, template_conditions=conditions, cost=cost)
        self.assertEquals(fee.amount, 0)

    def test_calc_multiply_each_page_by_unit_of_fifty_pages_returns_(self):
        details = ApplDetailsFactory(num_pages_drawings=1, num_pages_claims=1, num_pages_description=153)
        conditions = LineEstimationTemplateConditions(condition_pages_total_min=100)
        cmplxConds = ComplexConditionsFactory()
        cost = Money(100, 'USD')
        fee = cmplxConds.calc_multiply_each_page_by_unit_of_fifty_pages(
            appl_details=details, template_conditions=conditions, cost=cost)
        self.assertEquals(fee.amount, 100)

    def test_calc_multiply_each_page_by_unit_of_fifty_pages_returns_two(self):
        details = ApplDetailsFactory(num_pages_drawings=1, num_pages_claims=1, num_pages_description=300)
        conditions = LineEstimationTemplateConditions(condition_pages_total_min=20, condition_pages_total_max=120)
        cmplxConds = ComplexConditionsFactory()
        cost = Money(100, 'USD')
        fee = cmplxConds.calc_multiply_each_page_by_unit_of_fifty_pages(
            appl_details=details, template_conditions=conditions, cost=cost)
        self.assertEquals(fee.amount, 200)

    def test_calc_multiply_each_page_by_unit_of_fifty_pages_returns_six(self):
        details = ApplDetailsFactory(num_pages_drawings=1, num_pages_claims=1, num_pages_description=350)
        conditions = LineEstimationTemplateConditions(condition_pages_total_max=300)
        cmplxConds = ComplexConditionsFactory()
        cost = Money(100, 'USD')
        fee = cmplxConds.calc_multiply_each_page_by_unit_of_fifty_pages(
            appl_details=details, template_conditions=conditions, cost=cost)
        self.assertEquals(fee.amount, 600)


class TestEstimationUtils(TestCase):

    def test_utils__filter_fee_select_avail_currency_if_local_or_default(self):
        country_cn = CountryFactory(CN=True, currency_name='CNY')
        country_us = CountryFactory(US=True, currency_name='USD')
        appl = PCTApplicationFactory(country=country_cn, isa_country=country_us)

        conditions_true_AUD = factories.LineEstimationTemplateConditionsFactory(isa_country_fee_only=True)
        filing_est_template_true_AUD = factories.FilingEstimateTemplateFactory(conditions=conditions_true_AUD,
                                                                               official_cost=Money(100, 'AUD'))
        conditions_true_USD = factories.LineEstimationTemplateConditionsFactory(isa_country_fee_only=True)
        filing_est_template_true_USD = factories.FilingEstimateTemplateFactory(conditions=conditions_true_USD,
                                                                               official_cost=Money(40, 'USD'))
        templates = FilingEstimateTemplate.objects.all()
        filtered = utils._filter_fee_select_avail_currency_if_local_or_default(templates=templates, application=appl)
        self.assertEquals(len(filtered), 1)
        self.assertEquals(filtered.first(), filing_est_template_true_USD)

    def test_utils__filter_fee_select_avail_currency_if_local_or_default_return_one(self):
        country_cn = CountryFactory(CN=True, currency_name='CNY')
        country_us = CountryFactory(US=True, currency_name='USD')
        appl = PCTApplicationFactory(country=country_cn, isa_country=country_us)
        conditions_true_CNY = factories.LineEstimationTemplateConditionsFactory(isa_country_fee_only=True)
        filing_est_template_true_CNY = factories.FilingEstimateTemplateFactory(conditions=conditions_true_CNY,
                                                                               official_cost=Money(100, 'CNY'))
        conditions_true_USD = factories.LineEstimationTemplateConditionsFactory(isa_country_fee_only=True)
        filing_est_template_true_USD = factories.FilingEstimateTemplateFactory(conditions=conditions_true_USD,
                                                                               official_cost=Money(40, 'USD'))
        templates = FilingEstimateTemplate.objects.all()
        filtered = utils._filter_fee_select_avail_currency_if_local_or_default(templates=templates, application=appl)
        self.assertEquals(len(filtered), 1)
        self.assertEquals(filtered.first(), filing_est_template_true_CNY)

    def test_utils__filter_fee_select_avail_currency_if_local_or_default_returns_two(self):
        country_cn = CountryFactory(CN=True, currency_name='CNY')
        country_us = CountryFactory(US=True, currency_name='USD')
        appl = PCTApplicationFactory(country=country_cn, isa_country=country_us)
        conditions_true_CNY = factories.LineEstimationTemplateConditionsFactory(isa_country_fee_only=True)
        filing_est_template_true_CNY = factories.FilingEstimateTemplateFactory(conditions=conditions_true_CNY,
                                                                               official_cost=Money(100, 'CNY'))
        conditions_false_CNY = factories.LineEstimationTemplateConditionsFactory(isa_country_fee_only=False)
        filing_est_template_false_CNY = factories.FilingEstimateTemplateFactory(conditions=conditions_false_CNY,
                                                                                official_cost=Money(100, 'CNY'))
        conditions_false_USD = factories.LineEstimationTemplateConditionsFactory(isa_country_fee_only=True)
        filing_est_template_true_USD = factories.FilingEstimateTemplateFactory(conditions=conditions_false_USD,
                                                                               official_cost=Money(40, 'USD'))
        templates = FilingEstimateTemplate.objects.all()
        filtered = utils._filter_fee_select_avail_currency_if_local_or_default(templates=templates, application=appl)
        self.assertEquals(len(filtered), 2)

    def test_utils__filter_fee_entity_size_includes_correct_and_null_entity_size(self):
        entity_size_small = EntitySizeFactory(us_small=True)
        entity_size_micro = EntitySizeFactory(us_micro=True)
        conditions_small = factories.LineEstimationTemplateConditionsFactory(condition_entity_size=entity_size_small)
        conditions_micro = factories.LineEstimationTemplateConditionsFactory(condition_entity_size=entity_size_micro)
        conditions_none = factories.LineEstimationTemplateConditionsFactory()
        filing_est_template_small = factories.FilingEstimateTemplateFactory(conditions=conditions_small)
        filing_est_template_micro = factories.FilingEstimateTemplateFactory(conditions=conditions_micro)
        filing_est_template = factories.FilingEstimateTemplateFactory(conditions=conditions_none)
        templates = FilingEstimateTemplate.objects.all()
        appl_details = ApplDetailsFactory(entity_size=entity_size_small)
        application = BaseUtilityApplicationFactory(details=appl_details)
        filtered = utils._filter_entity_size(templates=templates, application=application, isa_filter=False)
        self.assertEquals(filtered.count(), 2)
        self.assertTrue(filtered.filter(conditions__condition_entity_size=entity_size_small).exists())
        self.assertTrue(filtered.filter(conditions__condition_entity_size=None).exists())

    def test_utils__filter_fee_entity_size_includes_only_null(self):
        entity_size_small = EntitySizeFactory(us_small=True)
        entity_size_micro = EntitySizeFactory(us_micro=True)
        conditions_small = factories.LineEstimationTemplateConditionsFactory(condition_entity_size=entity_size_small)
        conditions_micro = factories.LineEstimationTemplateConditionsFactory(condition_entity_size=entity_size_micro)
        conditions_none = factories.LineEstimationTemplateConditionsFactory()
        filing_est_template_small = factories.FilingEstimateTemplateFactory(conditions=conditions_small)
        filing_est_template_micro = factories.FilingEstimateTemplateFactory(conditions=conditions_micro)
        filing_est_template = factories.FilingEstimateTemplateFactory(conditions=conditions_none)
        templates = FilingEstimateTemplate.objects.all()
        appl_details = ApplDetailsFactory(entity_size=None)
        application = BaseUtilityApplicationFactory(details=appl_details)
        filtered = utils._filter_entity_size(templates=templates, application=application, isa_filter=False)
        self.assertEquals(filtered.count(), 1)
        self.assertEquals(filtered.first(), filing_est_template)
        self.assertTrue(filtered.filter(conditions__condition_entity_size=None).exists())

    def test_utils__filter_fee_entity_size_includes_correct_and_null_entity_size_for_ISA_Country(self):
        entity_size_small = EntitySizeFactory(us_small=True)
        entity_size_micro = EntitySizeFactory(us_micro=True)
        country_us = CountryFactory(US=True)
        country_cn = CountryFactory(CN=True)
        conditions_small = factories.LineEstimationTemplateConditionsFactory(condition_entity_size=entity_size_small)
        conditions_micro = factories.LineEstimationTemplateConditionsFactory(condition_entity_size=entity_size_micro)
        conditions_none = factories.LineEstimationTemplateConditionsFactory()
        filing_est_template_small = factories.FilingEstimateTemplateFactory(conditions=conditions_small)
        filing_est_template_micro = factories.FilingEstimateTemplateFactory(conditions=conditions_micro)
        filing_est_template = factories.FilingEstimateTemplateFactory(conditions=conditions_none)
        templates = FilingEstimateTemplate.objects.all()
        appl_details = ApplDetailsFactory(entity_size=entity_size_micro)
        application = PCTApplicationFactory(country=country_cn, isa_country=country_us,
                                            isa_entity_size=entity_size_small)
        filtered = utils._filter_entity_size(templates=templates, application=application, isa_filter=True)
        self.assertEquals(filtered.count(), 2)
        self.assertTrue(filtered.filter(conditions__condition_entity_size=entity_size_small).exists())
        self.assertTrue(filtered.filter(conditions__condition_entity_size=None).exists())

    def test_utils_filter_fee_doc_format_includes_correct_value_and_none(self):
        doc_format_electronic = DocFormatFactory(electronic=True)
        doc_format_paper = DocFormatFactory(paper=True)
        conditions_electronic = factories.LineEstimationTemplateConditionsFactory(doc_format=doc_format_electronic)
        conditions_paper = factories.LineEstimationTemplateConditionsFactory(doc_format=doc_format_paper)
        conditions_none = factories.LineEstimationTemplateConditionsFactory(doc_format=None)
        filing_est_template_electronic = factories.FilingEstimateTemplateFactory(conditions=conditions_electronic)
        filing_est_template_paper = factories.FilingEstimateTemplateFactory(conditions=conditions_paper)
        filing_est_template = factories.FilingEstimateTemplateFactory(conditions=conditions_none)
        templates = FilingEstimateTemplate.objects.all()
        particulars = ApplOptionsParticularsFactory(doc_format=doc_format_electronic)
        filtered = utils._filter_fee_doc_format(templates=templates, particulars=particulars)
        self.assertEquals(filtered.count(), 2)
        self.assertTrue(filtered.filter(conditions__doc_format=doc_format_electronic).exists())
        self.assertTrue(filtered.filter(conditions__doc_format=None).exists())

    def test_utils_filter_fee_doc_format_returns_only_none_with_special_doc_format(self):
        doc_format_electronic = DocFormatFactory(electronic=True)
        doc_format_paper = DocFormatFactory(paper=True)
        doc_format_unique_xml = DocFormatFactory(electronic_xml=True)
        conditions_electronic = factories.LineEstimationTemplateConditionsFactory(doc_format=doc_format_electronic)
        conditions_paper = factories.LineEstimationTemplateConditionsFactory(doc_format=doc_format_paper)
        conditions_none = factories.LineEstimationTemplateConditionsFactory(doc_format=None)
        filing_est_template_electronic = factories.FilingEstimateTemplateFactory(conditions=conditions_electronic)
        filing_est_template_paper = factories.FilingEstimateTemplateFactory(conditions=conditions_paper)
        filing_est_template = factories.FilingEstimateTemplateFactory(conditions=conditions_none)
        templates = FilingEstimateTemplate.objects.all()
        particulars = ApplOptionsParticularsFactory(doc_format=doc_format_unique_xml)
        filtered = utils._filter_fee_doc_format(templates=templates, particulars=particulars)
        self.assertEquals(filtered.count(), 1)
        self.assertEquals(filtered.first(), filing_est_template)
        self.assertTrue(filtered.filter(conditions__doc_format=None).exists())

    def test_utils_filter_fee_languages_includes_correct_value_and_none(self):
        language_cn = LanguageFactory(Chinese=True)
        language_en = LanguageFactory(English=True)
        conditions_chinese = factories.LineEstimationTemplateConditionsFactory(language=language_cn)
        conditions_english = factories.LineEstimationTemplateConditionsFactory(language=language_en)
        conditions_none = factories.LineEstimationTemplateConditionsFactory(doc_format=None)
        filing_est_template_chinese = factories.FilingEstimateTemplateFactory(conditions=conditions_chinese)
        filing_est_template_english = factories.FilingEstimateTemplateFactory(conditions=conditions_english)
        filing_est_template = factories.FilingEstimateTemplateFactory(conditions=conditions_none)
        templates = FilingEstimateTemplate.objects.all()
        appl_details = ApplDetailsFactory(language=language_cn)
        filtered = utils._filter_languages(templates=templates, appl_details=appl_details)
        self.assertEquals(filtered.count(), 2)
        self.assertTrue(filtered.filter(conditions__language=language_cn).exists())
        self.assertTrue(filtered.filter(conditions__language=None).exists())

    def test_utils_filter_fee_languages_includes_only_none(self):
        language_cn = LanguageFactory(Chinese=True)
        language_en = LanguageFactory(English=True)
        language_de = LanguageFactory(German=True)
        conditions_chinese = factories.LineEstimationTemplateConditionsFactory(language=language_cn)
        conditions_english = factories.LineEstimationTemplateConditionsFactory(language=language_en)
        conditions_none = factories.LineEstimationTemplateConditionsFactory(doc_format=None)
        filing_est_template_chinese = factories.FilingEstimateTemplateFactory(conditions=conditions_chinese)
        filing_est_template_english = factories.FilingEstimateTemplateFactory(conditions=conditions_english)
        filing_est_template = factories.FilingEstimateTemplateFactory(conditions=conditions_none)
        templates = FilingEstimateTemplate.objects.all()
        appl_details = ApplDetailsFactory(language=language_de)
        filtered = utils._filter_languages(templates=templates, appl_details=appl_details)
        self.assertEquals(filtered.count(), 1)
        self.assertEquals(filtered.first(), filing_est_template)
        self.assertTrue(filtered.filter(conditions__language=None).exists())

    def test_utils_filter_claims_all_three_returned(self):
        conditions_min_6 = factories.LineEstimationTemplateConditionsFactory(
            condition_claims_min=None,
            condition_claims_max=6)
        conditions_max_10 = factories.LineEstimationTemplateConditionsFactory(
            condition_claims_min=5,
            condition_claims_max=10)
        conditions_none = factories.LineEstimationTemplateConditionsFactory(
            condition_claims_min=None,
            condition_claims_max=None)
        filing_est_template_chinese = factories.FilingEstimateTemplateFactory(conditions=conditions_min_6)
        filing_est_template_english = factories.FilingEstimateTemplateFactory(conditions=conditions_max_10)
        filing_est_template = factories.FilingEstimateTemplateFactory(conditions=conditions_none)
        appl_details = ApplDetailsFactory(num_claims=6)
        templates = FilingEstimateTemplate.objects.all()
        filtered = utils._filter_claims(templates=templates, appl_details=appl_details)
        self.assertEquals(filtered.count(), 3)

    def test_utils_filter_claims_two_lower_returned(self):
        conditions_min_6 = factories.LineEstimationTemplateConditionsFactory(
            condition_claims_min=None,
            condition_claims_max=6)
        conditions_max_10 = factories.LineEstimationTemplateConditionsFactory(
            condition_claims_min=5,
            condition_claims_max=10)
        conditions_none = factories.LineEstimationTemplateConditionsFactory(
            condition_claims_min=None,
            condition_claims_max=None)
        filing_est_template_min_6 = factories.FilingEstimateTemplateFactory(conditions=conditions_min_6)
        filing_est_template_max_10 = factories.FilingEstimateTemplateFactory(conditions=conditions_max_10)
        filing_est_template = factories.FilingEstimateTemplateFactory(conditions=conditions_none)
        appl_details = ApplDetailsFactory(num_claims=4)
        templates = FilingEstimateTemplate.objects.all()
        filtered = utils._filter_claims(templates=templates, appl_details=appl_details)
        self.assertEquals(filtered.count(), 2)
        self.assertTrue(filtered.filter(conditions__condition_claims_max=None).exists())
        self.assertTrue(filtered.filter(conditions__condition_claims_max=6).exists())

    def test_utils_filter_claims_only_none_returned(self):
        conditions_min_6 = factories.LineEstimationTemplateConditionsFactory(
            condition_claims_min=None,
            condition_claims_max=6)
        conditions_max_10 = factories.LineEstimationTemplateConditionsFactory(
            condition_claims_min=5,
            condition_claims_max=10)
        conditions_none = factories.LineEstimationTemplateConditionsFactory(
            condition_claims_min=None,
            condition_claims_max=None)
        filing_est_template_min_6 = factories.FilingEstimateTemplateFactory(conditions=conditions_min_6)
        filing_est_template_max_10 = factories.FilingEstimateTemplateFactory(conditions=conditions_max_10)
        filing_est_template = factories.FilingEstimateTemplateFactory(conditions=conditions_none)
        appl_details = ApplDetailsFactory(num_claims=11)
        templates = FilingEstimateTemplate.objects.all()
        filtered = utils._filter_claims(templates=templates, appl_details=appl_details)
        self.assertEquals(filtered.count(), 1)
        self.assertEquals(filtered.first(), filing_est_template)

    def test_utils_filter_indep_claims_all_three_returned(self):
        conditions_min_6 = factories.LineEstimationTemplateConditionsFactory(
            condition_indep_claims_min=None,
            condition_indep_claims_max=6)
        conditions_max_10 = factories.LineEstimationTemplateConditionsFactory(
            condition_indep_claims_min=5,
            condition_indep_claims_max=10)
        conditions_none = factories.LineEstimationTemplateConditionsFactory(
            condition_indep_claims_min=None,
            condition_indep_claims_max=None)
        filing_est_template_chinese = factories.FilingEstimateTemplateFactory(conditions=conditions_min_6)
        filing_est_template_english = factories.FilingEstimateTemplateFactory(conditions=conditions_max_10)
        filing_est_template = factories.FilingEstimateTemplateFactory(conditions=conditions_none)
        appl_details = ApplDetailsFactory(num_indep_claims=6)
        templates = FilingEstimateTemplate.objects.all()
        filtered = utils._filter_indep_claims(templates=templates, appl_details=appl_details)
        self.assertEquals(filtered.count(), 3)

    def test_utils_filter_indep_claims_two_lower_returned(self):
        conditions_min_6 = factories.LineEstimationTemplateConditionsFactory(
            condition_indep_claims_min=None,
            condition_indep_claims_max=6)
        conditions_max_10 = factories.LineEstimationTemplateConditionsFactory(
            condition_indep_claims_min=5,
            condition_indep_claims_max=10)
        conditions_none = factories.LineEstimationTemplateConditionsFactory(
            condition_indep_claims_min=None,
            condition_indep_claims_max=None)
        filing_est_template_min_6 = factories.FilingEstimateTemplateFactory(conditions=conditions_min_6)
        filing_est_template_max_10 = factories.FilingEstimateTemplateFactory(conditions=conditions_max_10)
        filing_est_template = factories.FilingEstimateTemplateFactory(conditions=conditions_none)
        appl_details = ApplDetailsFactory(num_indep_claims=4)
        templates = FilingEstimateTemplate.objects.all()
        filtered = utils._filter_indep_claims(templates=templates, appl_details=appl_details)
        self.assertEquals(filtered.count(), 2)
        self.assertTrue(filtered.filter(conditions__condition_indep_claims_max=None).exists())
        self.assertTrue(filtered.filter(conditions__condition_indep_claims_max=6).exists())

    def test_utils_filter_indep_claims_only_none_returned(self):
        conditions_min_6 = factories.LineEstimationTemplateConditionsFactory(
            condition_indep_claims_min=None,
            condition_indep_claims_max=6)
        conditions_max_10 = factories.LineEstimationTemplateConditionsFactory(
            condition_indep_claims_min=5,
            condition_indep_claims_max=10)
        conditions_none = factories.LineEstimationTemplateConditionsFactory(
            condition_indep_claims_min=None,
            condition_indep_claims_max=None)
        filing_est_template_min_6 = factories.FilingEstimateTemplateFactory(conditions=conditions_min_6)
        filing_est_template_max_10 = factories.FilingEstimateTemplateFactory(conditions=conditions_max_10)
        filing_est_template = factories.FilingEstimateTemplateFactory(conditions=conditions_none)
        appl_details = ApplDetailsFactory(num_indep_claims=11)
        templates = FilingEstimateTemplate.objects.all()
        filtered = utils._filter_indep_claims(templates=templates, appl_details=appl_details)
        self.assertEquals(filtered.count(), 1)
        self.assertEquals(filtered.first(), filing_est_template)

    def test_utils_filter_claims_multiple_dependent_all_three_returned(self):
        conditions_min_6 = factories.LineEstimationTemplateConditionsFactory(
            condition_claims_multiple_dependent_min=None,
            condition_claims_multiple_dependent_max=6)
        conditions_max_10 = factories.LineEstimationTemplateConditionsFactory(
            condition_claims_multiple_dependent_min=5,
            condition_claims_multiple_dependent_max=10)
        conditions_none = factories.LineEstimationTemplateConditionsFactory(
            condition_claims_multiple_dependent_min=None,
            condition_claims_multiple_dependent_max=None)
        filing_est_template_chinese = factories.FilingEstimateTemplateFactory(conditions=conditions_min_6)
        filing_est_template_english = factories.FilingEstimateTemplateFactory(conditions=conditions_max_10)
        filing_est_template = factories.FilingEstimateTemplateFactory(conditions=conditions_none)
        appl_details = ApplDetailsFactory(num_claims_multiple_dependent=6)
        templates = FilingEstimateTemplate.objects.all()
        filtered = utils._filter_claims_multiple_dependent(templates=templates, appl_details=appl_details)
        self.assertEquals(filtered.count(), 3)

    def test_utils_filter_claims_multiple_dependent_two_lower_returned(self):
        conditions_min_6 = factories.LineEstimationTemplateConditionsFactory(
            condition_claims_multiple_dependent_min=None,
            condition_claims_multiple_dependent_max=6)
        conditions_max_10 = factories.LineEstimationTemplateConditionsFactory(
            condition_claims_multiple_dependent_min=5,
            condition_claims_multiple_dependent_max=10)
        conditions_none = factories.LineEstimationTemplateConditionsFactory(
            condition_claims_multiple_dependent_min=None,
            condition_claims_multiple_dependent_max=None)
        filing_est_template_min_6 = factories.FilingEstimateTemplateFactory(conditions=conditions_min_6)
        filing_est_template_max_10 = factories.FilingEstimateTemplateFactory(conditions=conditions_max_10)
        filing_est_template = factories.FilingEstimateTemplateFactory(conditions=conditions_none)
        appl_details = ApplDetailsFactory(num_claims_multiple_dependent=4)
        templates = FilingEstimateTemplate.objects.all()
        filtered = utils._filter_claims_multiple_dependent(templates=templates, appl_details=appl_details)
        self.assertEquals(filtered.count(), 2)
        self.assertTrue(filtered.filter(conditions__condition_claims_multiple_dependent_max=None).exists())
        self.assertTrue(filtered.filter(conditions__condition_claims_multiple_dependent_max=6).exists())

    def test_utils_filter_claims_multiple_dependent_only_none_returned(self):
        conditions_min_6 = factories.LineEstimationTemplateConditionsFactory(
            condition_claims_multiple_dependent_min=None,
            condition_claims_multiple_dependent_max=6)
        conditions_max_10 = factories.LineEstimationTemplateConditionsFactory(
            condition_claims_multiple_dependent_min=5,
            condition_claims_multiple_dependent_max=10)
        conditions_none = factories.LineEstimationTemplateConditionsFactory(
            condition_claims_multiple_dependent_min=None,
            condition_claims_multiple_dependent_max=None)
        filing_est_template_min_6 = factories.FilingEstimateTemplateFactory(conditions=conditions_min_6)
        filing_est_template_max_10 = factories.FilingEstimateTemplateFactory(conditions=conditions_max_10)
        filing_est_template = factories.FilingEstimateTemplateFactory(conditions=conditions_none)
        appl_details = ApplDetailsFactory(num_claims_multiple_dependent=11)
        templates = FilingEstimateTemplate.objects.all()
        filtered = utils._filter_claims_multiple_dependent(templates=templates, appl_details=appl_details)
        self.assertEquals(filtered.count(), 1)
        self.assertEquals(filtered.first(), filing_est_template)

    def test_utils_filter_total_pages_all_three_returned(self):
        conditions_min_6 = factories.LineEstimationTemplateConditionsFactory(
            condition_pages_total_min=None,
            condition_pages_total_max=6)
        conditions_max_10 = factories.LineEstimationTemplateConditionsFactory(
            condition_pages_total_min=5,
            condition_pages_total_max=10)
        conditions_none = factories.LineEstimationTemplateConditionsFactory(
            condition_pages_total_min=None,
            condition_pages_total_max=None)
        filing_est_template_chinese = factories.FilingEstimateTemplateFactory(conditions=conditions_min_6)
        filing_est_template_english = factories.FilingEstimateTemplateFactory(conditions=conditions_max_10)
        filing_est_template = factories.FilingEstimateTemplateFactory(conditions=conditions_none)
        appl_details = ApplDetailsFactory(num_pages_description=2, num_pages_claims=2, num_pages_drawings=2)
        templates = FilingEstimateTemplate.objects.all()
        filtered = utils._filter_total_pages(templates=templates, appl_details=appl_details)
        self.assertEquals(filtered.count(), 3)

    def test_utils_filter_total_pages_two_lower_returned(self):
        conditions_min_6 = factories.LineEstimationTemplateConditionsFactory(
            condition_pages_total_min=None,
            condition_pages_total_max=6)
        conditions_max_10 = factories.LineEstimationTemplateConditionsFactory(
            condition_pages_total_min=5,
            condition_pages_total_max=10)
        conditions_none = factories.LineEstimationTemplateConditionsFactory(
            condition_pages_total_min=None,
            condition_pages_total_max=None)
        filing_est_template_min_6 = factories.FilingEstimateTemplateFactory(conditions=conditions_min_6)
        filing_est_template_max_10 = factories.FilingEstimateTemplateFactory(conditions=conditions_max_10)
        filing_est_template = factories.FilingEstimateTemplateFactory(conditions=conditions_none)
        appl_details = ApplDetailsFactory(num_pages_description=2, num_pages_claims=1, num_pages_drawings=1)
        templates = FilingEstimateTemplate.objects.all()
        filtered = utils._filter_total_pages(templates=templates, appl_details=appl_details)
        self.assertEquals(filtered.count(), 2)
        self.assertTrue(filtered.filter(conditions__condition_pages_total_max=None).exists())
        self.assertTrue(filtered.filter(conditions__condition_pages_total_max=6).exists())

    def test_utils_filter_total_pages_only_none_returned(self):
        conditions_min_6 = factories.LineEstimationTemplateConditionsFactory(
            condition_pages_total_min=None,
            condition_pages_total_max=6)
        conditions_max_10 = factories.LineEstimationTemplateConditionsFactory(
            condition_pages_total_min=5,
            condition_pages_total_max=10)
        conditions_none = factories.LineEstimationTemplateConditionsFactory(
            condition_pages_total_min=None,
            condition_pages_total_max=None)
        filing_est_template_min_6 = factories.FilingEstimateTemplateFactory(conditions=conditions_min_6)
        filing_est_template_max_10 = factories.FilingEstimateTemplateFactory(conditions=conditions_max_10)
        filing_est_template = factories.FilingEstimateTemplateFactory(conditions=conditions_none)
        appl_details = ApplDetailsFactory(num_pages_description=7, num_pages_claims=2, num_pages_drawings=2)
        templates = FilingEstimateTemplate.objects.all()
        filtered = utils._filter_total_pages(templates=templates, appl_details=appl_details)
        self.assertEquals(filtered.count(), 1)
        self.assertEquals(filtered.first(), filing_est_template)

    def test_utils_filter_desc_pages_all_three_returned(self):
        conditions_min_6 = factories.LineEstimationTemplateConditionsFactory(
            condition_pages_desc_min=None,
            condition_pages_desc_max=6)
        conditions_max_10 = factories.LineEstimationTemplateConditionsFactory(
            condition_pages_desc_min=5,
            condition_pages_desc_max=10)
        conditions_none = factories.LineEstimationTemplateConditionsFactory(
            condition_pages_desc_min=None,
            condition_pages_desc_max=None)
        filing_est_template_chinese = factories.FilingEstimateTemplateFactory(conditions=conditions_min_6)
        filing_est_template_english = factories.FilingEstimateTemplateFactory(conditions=conditions_max_10)
        filing_est_template = factories.FilingEstimateTemplateFactory(conditions=conditions_none)
        appl_details = ApplDetailsFactory(num_pages_description=6)
        templates = FilingEstimateTemplate.objects.all()
        filtered = utils._filter_desc_pages(templates=templates, appl_details=appl_details)
        self.assertEquals(filtered.count(), 3)

    def test_utils_filter_desc_pages_two_lower_returned(self):
        conditions_min_6 = factories.LineEstimationTemplateConditionsFactory(
            condition_pages_desc_min=None,
            condition_pages_desc_max=6)
        conditions_max_10 = factories.LineEstimationTemplateConditionsFactory(
            condition_pages_desc_min=5,
            condition_pages_desc_max=10)
        conditions_none = factories.LineEstimationTemplateConditionsFactory(
            condition_pages_desc_min=None,
            condition_pages_desc_max=None)
        filing_est_template_min_6 = factories.FilingEstimateTemplateFactory(conditions=conditions_min_6)
        filing_est_template_max_10 = factories.FilingEstimateTemplateFactory(conditions=conditions_max_10)
        filing_est_template = factories.FilingEstimateTemplateFactory(conditions=conditions_none)
        appl_details = ApplDetailsFactory(num_pages_description=4)
        templates = FilingEstimateTemplate.objects.all()
        filtered = utils._filter_desc_pages(templates=templates, appl_details=appl_details)
        self.assertEquals(filtered.count(), 2)
        self.assertTrue(filtered.filter(conditions__condition_pages_desc_max=None).exists())
        self.assertTrue(filtered.filter(conditions__condition_pages_desc_max=6).exists())

    def test_utils_filter_desc_pages_only_none_returned(self):
        conditions_min_6 = factories.LineEstimationTemplateConditionsFactory(
            condition_pages_desc_min=None,
            condition_pages_desc_max=6)
        conditions_max_10 = factories.LineEstimationTemplateConditionsFactory(
            condition_pages_desc_min=5,
            condition_pages_desc_max=10)
        conditions_none = factories.LineEstimationTemplateConditionsFactory(
            condition_pages_desc_min=None,
            condition_pages_desc_max=None)
        filing_est_template_min_6 = factories.FilingEstimateTemplateFactory(conditions=conditions_min_6)
        filing_est_template_max_10 = factories.FilingEstimateTemplateFactory(conditions=conditions_max_10)
        filing_est_template = factories.FilingEstimateTemplateFactory(conditions=conditions_none)
        appl_details = ApplDetailsFactory(num_pages_description=11)
        templates = FilingEstimateTemplate.objects.all()
        filtered = utils._filter_desc_pages(templates=templates, appl_details=appl_details)
        self.assertEquals(filtered.count(), 1)
        self.assertEquals(filtered.first(), filing_est_template)

    def test_utils_filter_claims_pages_all_three_returned(self):
        conditions_min_6 = factories.LineEstimationTemplateConditionsFactory(
            condition_pages_claims_min=None,
            condition_pages_claims_max=6)
        conditions_max_10 = factories.LineEstimationTemplateConditionsFactory(
            condition_pages_claims_min=5,
            condition_pages_claims_max=10)
        conditions_none = factories.LineEstimationTemplateConditionsFactory(
            condition_pages_claims_min=None,
            condition_pages_claims_max=None)
        filing_est_template_chinese = factories.FilingEstimateTemplateFactory(conditions=conditions_min_6)
        filing_est_template_english = factories.FilingEstimateTemplateFactory(conditions=conditions_max_10)
        filing_est_template = factories.FilingEstimateTemplateFactory(conditions=conditions_none)
        appl_details = ApplDetailsFactory(num_pages_claims=6)
        templates = FilingEstimateTemplate.objects.all()
        filtered = utils._filter_claims_pages(templates=templates, appl_details=appl_details)
        self.assertEquals(filtered.count(), 3)

    def test_utils_filter_claims_pages_two_lower_returned(self):
        conditions_min_6 = factories.LineEstimationTemplateConditionsFactory(
            condition_pages_claims_min=None,
            condition_pages_claims_max=6)
        conditions_max_10 = factories.LineEstimationTemplateConditionsFactory(
            condition_pages_claims_min=5,
            condition_pages_claims_max=10)
        conditions_none = factories.LineEstimationTemplateConditionsFactory(
            condition_pages_claims_min=None,
            condition_pages_claims_max=None)
        filing_est_template_min_6 = factories.FilingEstimateTemplateFactory(conditions=conditions_min_6)
        filing_est_template_max_10 = factories.FilingEstimateTemplateFactory(conditions=conditions_max_10)
        filing_est_template = factories.FilingEstimateTemplateFactory(conditions=conditions_none)
        appl_details = ApplDetailsFactory(num_pages_claims=4)
        templates = FilingEstimateTemplate.objects.all()
        filtered = utils._filter_claims_pages(templates=templates, appl_details=appl_details)
        self.assertEquals(filtered.count(), 2)
        self.assertTrue(filtered.filter(conditions__condition_pages_claims_max=None).exists())
        self.assertTrue(filtered.filter(conditions__condition_pages_claims_max=6).exists())

    def test_utils_filter_claims_pages_only_none_returned(self):
        conditions_min_6 = factories.LineEstimationTemplateConditionsFactory(
            condition_pages_claims_min=None,
            condition_pages_claims_max=6)
        conditions_max_10 = factories.LineEstimationTemplateConditionsFactory(
            condition_pages_claims_min=5,
            condition_pages_claims_max=10)
        conditions_none = factories.LineEstimationTemplateConditionsFactory(
            condition_pages_claims_min=None,
            condition_pages_claims_max=None)
        filing_est_template_min_6 = factories.FilingEstimateTemplateFactory(conditions=conditions_min_6)
        filing_est_template_max_10 = factories.FilingEstimateTemplateFactory(conditions=conditions_max_10)
        filing_est_template = factories.FilingEstimateTemplateFactory(conditions=conditions_none)
        appl_details = ApplDetailsFactory(num_pages_claims=11)
        templates = FilingEstimateTemplate.objects.all()
        filtered = utils._filter_claims_pages(templates=templates, appl_details=appl_details)
        self.assertEquals(filtered.count(), 1)
        self.assertEquals(filtered.first(), filing_est_template)

    def test_utils_filter_drawings_pages_all_three_returned(self):
        conditions_min_6 = factories.LineEstimationTemplateConditionsFactory(
            condition_pages_drawings_min=None,
            condition_pages_drawings_max=6)
        conditions_max_10 = factories.LineEstimationTemplateConditionsFactory(
            condition_pages_drawings_min=5,
            condition_pages_drawings_max=10)
        conditions_none = factories.LineEstimationTemplateConditionsFactory(
            condition_pages_drawings_min=None,
            condition_pages_drawings_max=None)
        filing_est_template_chinese = factories.FilingEstimateTemplateFactory(conditions=conditions_min_6)
        filing_est_template_english = factories.FilingEstimateTemplateFactory(conditions=conditions_max_10)
        filing_est_template = factories.FilingEstimateTemplateFactory(conditions=conditions_none)
        appl_details = ApplDetailsFactory(num_pages_drawings=6)
        templates = FilingEstimateTemplate.objects.all()
        filtered = utils._filter_drawings_pages(templates=templates, appl_details=appl_details)
        self.assertEquals(filtered.count(), 3)

    def test_utils_filter_drawings_pages_two_lower_returned(self):
        conditions_min_6 = factories.LineEstimationTemplateConditionsFactory(
            condition_pages_drawings_min=None,
            condition_pages_drawings_max=6)
        conditions_max_10 = factories.LineEstimationTemplateConditionsFactory(
            condition_pages_drawings_min=5,
            condition_pages_drawings_max=10)
        conditions_none = factories.LineEstimationTemplateConditionsFactory(
            condition_pages_drawings_min=None,
            condition_pages_drawings_max=None)
        filing_est_template_min_6 = factories.FilingEstimateTemplateFactory(conditions=conditions_min_6)
        filing_est_template_max_10 = factories.FilingEstimateTemplateFactory(conditions=conditions_max_10)
        filing_est_template = factories.FilingEstimateTemplateFactory(conditions=conditions_none)
        appl_details = ApplDetailsFactory(num_pages_drawings=4)
        templates = FilingEstimateTemplate.objects.all()
        filtered = utils._filter_drawings_pages(templates=templates, appl_details=appl_details)
        self.assertEquals(filtered.count(), 2)
        self.assertTrue(filtered.filter(conditions__condition_pages_drawings_max=None).exists())
        self.assertTrue(filtered.filter(conditions__condition_pages_drawings_max=6).exists())

    def test_utils_filter_drawings_pages_only_none_returned(self):
        conditions_min_6 = factories.LineEstimationTemplateConditionsFactory(
            condition_pages_drawings_min=None,
            condition_pages_drawings_max=6)
        conditions_max_10 = factories.LineEstimationTemplateConditionsFactory(
            condition_pages_drawings_min=5,
            condition_pages_drawings_max=10)
        conditions_none = factories.LineEstimationTemplateConditionsFactory(
            condition_pages_drawings_min=None,
            condition_pages_drawings_max=None)
        filing_est_template_min_6 = factories.FilingEstimateTemplateFactory(conditions=conditions_min_6)
        filing_est_template_max_10 = factories.FilingEstimateTemplateFactory(conditions=conditions_max_10)
        filing_est_template = factories.FilingEstimateTemplateFactory(conditions=conditions_none)
        appl_details = ApplDetailsFactory(num_pages_drawings=11)
        templates = FilingEstimateTemplate.objects.all()
        filtered = utils._filter_drawings_pages(templates=templates, appl_details=appl_details)
        self.assertEquals(filtered.count(), 1)
        self.assertEquals(filtered.first(), filing_est_template)

    def test_utils_filter_drawings_all_three_returned(self):
        conditions_min_6 = factories.LineEstimationTemplateConditionsFactory(
            condition_drawings_min=None,
            condition_drawings_max=6)
        conditions_max_10 = factories.LineEstimationTemplateConditionsFactory(
            condition_drawings_min=5,
            condition_drawings_max=10)
        conditions_none = factories.LineEstimationTemplateConditionsFactory(
            condition_drawings_min=None,
            condition_drawings_max=None)
        filing_est_template_chinese = factories.FilingEstimateTemplateFactory(conditions=conditions_min_6)
        filing_est_template_english = factories.FilingEstimateTemplateFactory(conditions=conditions_max_10)
        filing_est_template = factories.FilingEstimateTemplateFactory(conditions=conditions_none)
        appl_details = ApplDetailsFactory(num_drawings=6)
        templates = FilingEstimateTemplate.objects.all()
        filtered = utils._filter_drawings(templates=templates, appl_details=appl_details)
        self.assertEquals(filtered.count(), 3)

    def test_utils_filter_drawings_two_lower_returned(self):
        conditions_min_6 = factories.LineEstimationTemplateConditionsFactory(
            condition_drawings_min=None,
            condition_drawings_max=6)
        conditions_max_10 = factories.LineEstimationTemplateConditionsFactory(
            condition_drawings_min=5,
            condition_drawings_max=10)
        conditions_none = factories.LineEstimationTemplateConditionsFactory(
            condition_drawings_min=None,
            condition_drawings_max=None)
        filing_est_template_min_6 = factories.FilingEstimateTemplateFactory(conditions=conditions_min_6)
        filing_est_template_max_10 = factories.FilingEstimateTemplateFactory(conditions=conditions_max_10)
        filing_est_template = factories.FilingEstimateTemplateFactory(conditions=conditions_none)
        appl_details = ApplDetailsFactory(num_drawings=4)
        templates = FilingEstimateTemplate.objects.all()
        filtered = utils._filter_drawings(templates=templates, appl_details=appl_details)
        self.assertEquals(filtered.count(), 2)
        self.assertTrue(filtered.filter(conditions__condition_drawings_max=None).exists())
        self.assertTrue(filtered.filter(conditions__condition_drawings_max=6).exists())

    def test_utils_filter_drawings_only_none_returned(self):
        conditions_min_6 = factories.LineEstimationTemplateConditionsFactory(
            condition_drawings_min=None,
            condition_drawings_max=6)
        conditions_max_10 = factories.LineEstimationTemplateConditionsFactory(
            condition_drawings_min=5,
            condition_drawings_max=10)
        conditions_none = factories.LineEstimationTemplateConditionsFactory(
            condition_drawings_min=None,
            condition_drawings_max=None)
        filing_est_template_min_6 = factories.FilingEstimateTemplateFactory(conditions=conditions_min_6)
        filing_est_template_max_10 = factories.FilingEstimateTemplateFactory(conditions=conditions_max_10)
        filing_est_template = factories.FilingEstimateTemplateFactory(conditions=conditions_none)
        appl_details = ApplDetailsFactory(num_drawings=11)
        templates = FilingEstimateTemplate.objects.all()
        filtered = utils._filter_drawings(templates=templates, appl_details=appl_details)
        self.assertEquals(filtered.count(), 1)
        self.assertEquals(filtered.first(), filing_est_template)

    def test_utils_filter_annual_prosecution_fee_returns_three(self):
        appl_option = ApplOptionsFactory()
        publ_option = PublOptionFactory(appl=appl_option, date_diff='P10M')
        request_option = RequestExaminationOptionFactory(appl=appl_option, date_diff='P10M')
        oa_option = OAOptionsFactory(appl=appl_option, date_diff='P10M')
        allow_option = AllowOptionsFactory(appl=appl_option, date_diff='P10M')
        issue_option = IssueOptionsFactory(appl=appl_option, date_diff='P10M')

        conditions_true = factories.LineEstimationTemplateConditionsFactory(condition_annual_prosecution_fee=True)
        conditions_true_2 = factories.LineEstimationTemplateConditionsFactory(condition_annual_prosecution_fee=True)
        conditions_true_3 = factories.LineEstimationTemplateConditionsFactory(condition_annual_prosecution_fee=True)
        conditions_true_4 = factories.LineEstimationTemplateConditionsFactory(condition_annual_prosecution_fee=True)
        conditions_false = factories.LineEstimationTemplateConditionsFactory(condition_annual_prosecution_fee=False)
        filing_est_template_cond_true = factories.FilingEstimateTemplateFactory(date_diff='P1Y',
                                                                                conditions=conditions_true)
        filing_est_template_cond_true_2 = factories.FilingEstimateTemplateFactory(date_diff='P2Y',
                                                                                  conditions=conditions_true_2)
        filing_est_template_cond_true_3 = factories.FilingEstimateTemplateFactory(date_diff='P3Y',
                                                                                  conditions=conditions_true_3)
        filing_est_template_cond_true_4 = factories.FilingEstimateTemplateFactory(date_diff='P4Y',
                                                                                  conditions=conditions_true_4)
        filing_est_template_false = factories.FilingEstimateTemplateFactory(date_diff='P1Y',
                                                                            conditions=conditions_false)

        total_date_diff = request_option.date_diff + oa_option.date_diff + allow_option.date_diff
        application = BaseUtilityApplicationFactory(date_filing=date(2010, 1, 1))
        publication = PublicationFactory(application=application, date_publication=date(2011, 6, 1))
        req_exam = RequestExaminationFactory(application=application, date_request_examination=date(2010, 6, 1))
        oa = OfficeActionFactory(application=application, date_office_action=date(2012, 1, 4))
        allowance = AllowanceFactory(application=application, date_allowance=date(2012, 9, 12))
        issuance = IssuanceFactory(application=application, date_issuance=date(2014, 5, 1))

        templates = FilingEstimateTemplate.objects.all()
        filtered = utils._filter_annual_prosecution_fee(templates=templates, application=application)
        self.assertEquals(filtered.count(), 3)
        self.assertIn(filing_est_template_cond_true, filtered)
        self.assertIn(filing_est_template_cond_true_2, filtered)
        self.assertIn(filing_est_template_false, filtered)

    def test_utils_filter_annual_prosecution_fee_returns_four(self):
        appl_option = ApplOptionsFactory()
        publ_option = PublOptionFactory(appl=appl_option, date_diff='P20M')
        request_option = RequestExaminationOptionFactory(appl=appl_option, date_diff='P20M')
        oa_option = OAOptionsFactory(appl=appl_option, date_diff='P10M')
        allow_option = AllowOptionsFactory(appl=appl_option, date_diff='P10M')
        issue_option = IssueOptionsFactory(appl=appl_option, date_diff='P10M')

        conditions_true = factories.LineEstimationTemplateConditionsFactory(condition_annual_prosecution_fee=True)
        conditions_true_2 = factories.LineEstimationTemplateConditionsFactory(condition_annual_prosecution_fee=True)
        conditions_true_3 = factories.LineEstimationTemplateConditionsFactory(condition_annual_prosecution_fee=True)
        conditions_true_4 = factories.LineEstimationTemplateConditionsFactory(condition_annual_prosecution_fee=True)
        conditions_false = factories.LineEstimationTemplateConditionsFactory(condition_annual_prosecution_fee=False)
        filing_est_template_cond_true = factories.FilingEstimateTemplateFactory(date_diff='P1Y',
                                                                                conditions=conditions_true)
        filing_est_template_cond_true_2 = factories.FilingEstimateTemplateFactory(date_diff='P2Y',
                                                                                  conditions=conditions_true_2)
        filing_est_template_cond_true_3 = factories.FilingEstimateTemplateFactory(date_diff='P3Y',
                                                                                  conditions=conditions_true_3)
        filing_est_template_cond_true_4 = factories.FilingEstimateTemplateFactory(date_diff='P4Y',
                                                                                  conditions=conditions_true_4)
        filing_est_template_false = factories.FilingEstimateTemplateFactory(date_diff='P1Y',
                                                                            conditions=conditions_false)

        total_date_diff = request_option.date_diff + oa_option.date_diff + allow_option.date_diff
        application = BaseUtilityApplicationFactory(date_filing=date(2010, 1, 1))
        publication = PublicationFactory(application=application, date_publication=date(2011, 6, 1))
        req_exam = RequestExaminationFactory(application=application, date_request_examination=date(2010, 6, 1))
        oa = OfficeActionFactory(application=application, date_office_action=date(2012, 1, 4))
        allowance = AllowanceFactory(application=application, date_allowance=date(2013, 9, 12))
        issuance = IssuanceFactory(application=application, date_issuance=date(2014, 5, 1))

        templates = FilingEstimateTemplate.objects.all()
        filtered = utils._filter_annual_prosecution_fee(templates=templates, application=application)
        self.assertEquals(filtered.count(), 4)
        self.assertIn(filing_est_template_cond_true, filtered)
        self.assertIn(filing_est_template_cond_true_2, filtered)
        self.assertIn(filing_est_template_cond_true_3, filtered)
        self.assertIn(filing_est_template_false, filtered)

    def test_utils_filter_annual_prosecution_fee_until_grant_returns_four(self):
        appl_option = ApplOptionsFactory()
        publ_option = PublOptionFactory(appl=appl_option, date_diff='P10M')
        request_option = RequestExaminationOptionFactory(appl=appl_option, date_diff='P10M')
        oa_option = OAOptionsFactory(appl=appl_option, date_diff='P10M')
        allow_option = AllowOptionsFactory(appl=appl_option, date_diff='P10M')
        issue_option = IssueOptionsFactory(appl=appl_option, date_diff='P10M')

        conditions_true = factories.LineEstimationTemplateConditionsFactory(
            condition_annual_prosecution_fee_until_grant=True)
        conditions_true_2 = factories.LineEstimationTemplateConditionsFactory(
            condition_annual_prosecution_fee_until_grant=True)
        conditions_true_3 = factories.LineEstimationTemplateConditionsFactory(
            condition_annual_prosecution_fee_until_grant=True)
        conditions_true_4 = factories.LineEstimationTemplateConditionsFactory(
            condition_annual_prosecution_fee_until_grant=True)
        conditions_true_5 = factories.LineEstimationTemplateConditionsFactory(
            condition_annual_prosecution_fee_until_grant=True)
        conditions_false = factories.LineEstimationTemplateConditionsFactory(
            condition_annual_prosecution_fee_until_grant=False)
        filing_est_template_cond_true = factories.FilingEstimateTemplateFactory(date_diff='P1Y',
                                                                                conditions=conditions_true)
        filing_est_template_cond_true_2 = factories.FilingEstimateTemplateFactory(date_diff='P2Y',
                                                                                  conditions=conditions_true_2)
        filing_est_template_cond_true_3 = factories.FilingEstimateTemplateFactory(date_diff='P3Y',
                                                                                  conditions=conditions_true_3)
        filing_est_template_cond_true_4 = factories.FilingEstimateTemplateFactory(date_diff='P4Y',
                                                                                  conditions=conditions_true_4)
        filing_est_template_cond_true_5 = factories.FilingEstimateTemplateFactory(date_diff='P5Y',
                                                                                  conditions=conditions_true_5)
        filing_est_template_false = factories.FilingEstimateTemplateFactory(date_diff='P1Y',
                                                                            conditions=conditions_false)

        total_date_diff = request_option.date_diff + oa_option.date_diff + allow_option.date_diff
        # P30M
        application = BaseUtilityApplicationFactory(date_filing=date(2010, 1, 1))
        publication = PublicationFactory(application=application, date_publication=date(2011, 6, 1))
        req_exam = RequestExaminationFactory(application=application, date_request_examination=date(2010, 6, 1))
        oa = OfficeActionFactory(application=application, date_office_action=date(2012, 1, 4))
        allowance = AllowanceFactory(application=application, date_allowance=date(2012, 9, 12))
        issuance = IssuanceFactory(application=application, date_issuance=date(2013, 5, 1))
        templates = FilingEstimateTemplate.objects.all()
        filtered = utils._filter_annual_prosecution_fee_until_grant(templates=templates, application=application)
        self.assertEquals(filtered.count(), 4)
        self.assertIn(filing_est_template_cond_true, filtered)
        self.assertIn(filing_est_template_cond_true_2, filtered)
        self.assertIn(filing_est_template_cond_true_3, filtered)
        self.assertIn(filing_est_template_false, filtered)

    def test_utils_filter_annual_prosecution_fee_until_grant_returns_five(self):
        appl_option = ApplOptionsFactory()
        publ_option = PublOptionFactory(appl=appl_option, date_diff='P10M')
        request_option = RequestExaminationOptionFactory(appl=appl_option, date_diff='P20M')
        oa_option = OAOptionsFactory(appl=appl_option, date_diff='P10M')
        allow_option = AllowOptionsFactory(appl=appl_option, date_diff='P10M')
        issue_option = IssueOptionsFactory(appl=appl_option, date_diff='P10M')

        conditions_true = factories.LineEstimationTemplateConditionsFactory(
            condition_annual_prosecution_fee_until_grant=True)
        conditions_true_2 = factories.LineEstimationTemplateConditionsFactory(
            condition_annual_prosecution_fee_until_grant=True)
        conditions_true_3 = factories.LineEstimationTemplateConditionsFactory(
            condition_annual_prosecution_fee_until_grant=True)
        conditions_true_4 = factories.LineEstimationTemplateConditionsFactory(
            condition_annual_prosecution_fee_until_grant=True)
        conditions_true_5 = factories.LineEstimationTemplateConditionsFactory(
            condition_annual_prosecution_fee_until_grant=True)
        conditions_false = factories.LineEstimationTemplateConditionsFactory(
            condition_annual_prosecution_fee_until_grant=False)
        filing_est_template_cond_true = factories.FilingEstimateTemplateFactory(date_diff='P1Y',
                                                                                conditions=conditions_true)
        filing_est_template_cond_true_2 = factories.FilingEstimateTemplateFactory(date_diff='P2Y',
                                                                                  conditions=conditions_true_2)
        filing_est_template_cond_true_3 = factories.FilingEstimateTemplateFactory(date_diff='P3Y',
                                                                                  conditions=conditions_true_3)
        filing_est_template_cond_true_4 = factories.FilingEstimateTemplateFactory(date_diff='P4Y',
                                                                                  conditions=conditions_true_4)
        filing_est_template_cond_true_5 = factories.FilingEstimateTemplateFactory(date_diff='P5Y',
                                                                                  conditions=conditions_true_5)
        filing_est_template_false = factories.FilingEstimateTemplateFactory(date_diff='P1Y',
                                                                            conditions=conditions_false)

        total_date_diff = request_option.date_diff + oa_option.date_diff + allow_option.date_diff
        # P30M
        application = BaseUtilityApplicationFactory(date_filing=date(2010, 1, 1))
        publication = PublicationFactory(application=application, date_publication=date(2011, 6, 1))
        req_exam = RequestExaminationFactory(application=application, date_request_examination=date(2010, 6, 1))
        oa = OfficeActionFactory(application=application, date_office_action=date(2012, 1, 4))
        allowance = AllowanceFactory(application=application, date_allowance=date(2012, 9, 12))
        issuance = IssuanceFactory(application=application, date_issuance=date(2014, 5, 1))
        templates = FilingEstimateTemplate.objects.all()
        filtered = utils._filter_annual_prosecution_fee_until_grant(templates=templates, application=application)
        self.assertEquals(filtered.count(), 5)
        self.assertIn(filing_est_template_cond_true, filtered)
        self.assertIn(filing_est_template_cond_true_2, filtered)
        self.assertIn(filing_est_template_cond_true_3, filtered)
        self.assertIn(filing_est_template_cond_true_4, filtered)
        self.assertIn(filing_est_template_false, filtered)

    def test_utils_filter_renewal_fee_from_filing_after_grant_returns_three(self):
        appl_option = ApplOptionsFactory()
        publ_option = PublOptionFactory(appl=appl_option, date_diff='P10M')
        request_option = RequestExaminationOptionFactory(appl=appl_option, date_diff='P10M')
        oa_option = OAOptionsFactory(appl=appl_option, date_diff='P10M')
        allow_option = AllowOptionsFactory(appl=appl_option, date_diff='P10M')
        issue_option = IssueOptionsFactory(appl=appl_option, date_diff='P10M')

        conditions_true = factories.LineEstimationTemplateConditionsFactory(
            condition_renewal_fee_from_filing_after_grant=True)
        conditions_true_2 = factories.LineEstimationTemplateConditionsFactory(
            condition_renewal_fee_from_filing_after_grant=True)
        conditions_true_3 = factories.LineEstimationTemplateConditionsFactory(
            condition_renewal_fee_from_filing_after_grant=True)
        conditions_true_4 = factories.LineEstimationTemplateConditionsFactory(
            condition_renewal_fee_from_filing_after_grant=True)
        conditions_true_5 = factories.LineEstimationTemplateConditionsFactory(
            condition_renewal_fee_from_filing_after_grant=True)
        conditions_false = factories.LineEstimationTemplateConditionsFactory(
            condition_renewal_fee_from_filing_after_grant=False)
        filing_est_template_cond_true = factories.FilingEstimateTemplateFactory(date_diff='P1Y',
                                                                                conditions=conditions_true)
        filing_est_template_cond_true_2 = factories.FilingEstimateTemplateFactory(date_diff='P2Y',
                                                                                  conditions=conditions_true_2)
        filing_est_template_cond_true_3 = factories.FilingEstimateTemplateFactory(date_diff='P3Y',
                                                                                  conditions=conditions_true_3)
        filing_est_template_cond_true_4 = factories.FilingEstimateTemplateFactory(date_diff='P4Y',
                                                                                  conditions=conditions_true_4)
        filing_est_template_cond_true_5 = factories.FilingEstimateTemplateFactory(date_diff='P5Y',
                                                                                  conditions=conditions_true_5)
        filing_est_template_false = factories.FilingEstimateTemplateFactory(date_diff='P1Y',
                                                                            conditions=conditions_false)

        total_date_diff = request_option.date_diff + oa_option.date_diff + allow_option.date_diff
        # P30M
        templates = FilingEstimateTemplate.objects.all()
        # filtered = utils._filter_renewal_fee_from_filing_after_grant(templates=templates, appl_option=appl_option)
        application = BaseUtilityApplicationFactory(date_filing=date(2010, 1, 1))
        publication = PublicationFactory(application=application, date_publication=date(2011, 6, 1))
        req_exam = RequestExaminationFactory(application=application, date_request_examination=date(2010, 6, 1))
        oa = OfficeActionFactory(application=application, date_office_action=date(2012, 1, 4))
        allowance = AllowanceFactory(application=application, date_allowance=date(2012, 9, 12))
        issuance = IssuanceFactory(application=application, date_issuance=date(2013, 1, 1))
        filtered = utils._filter_renewal_fee_from_filing_after_grant(templates=templates, application=application)
        self.assertEquals(filtered.count(), 3)
        # self.assertIn(filing_est_template_cond_true, filtered)
        # self.assertIn(filing_est_template_cond_true_2, filtered)
        # self.assertIn(filing_est_template_cond_true_3, filtered)
        self.assertIn(filing_est_template_cond_true_4, filtered)
        self.assertIn(filing_est_template_cond_true_5, filtered)
        self.assertIn(filing_est_template_false, filtered)

    def test_utils_filter_renewal_fee_from_filing_after_grant_returns_two(self):
        appl_option = ApplOptionsFactory()
        publ_option = PublOptionFactory(appl=appl_option, date_diff='P10M')
        request_option = RequestExaminationOptionFactory(appl=appl_option, date_diff='P10M')
        oa_option = OAOptionsFactory(appl=appl_option, date_diff='P10M')
        allow_option = AllowOptionsFactory(appl=appl_option, date_diff='P10M')
        issue_option = IssueOptionsFactory(appl=appl_option, date_diff='P10M')

        conditions_true = factories.LineEstimationTemplateConditionsFactory(
            condition_renewal_fee_from_filing_after_grant=True)
        conditions_true_2 = factories.LineEstimationTemplateConditionsFactory(
            condition_renewal_fee_from_filing_after_grant=True)
        conditions_true_3 = factories.LineEstimationTemplateConditionsFactory(
            condition_renewal_fee_from_filing_after_grant=True)
        conditions_true_4 = factories.LineEstimationTemplateConditionsFactory(
            condition_renewal_fee_from_filing_after_grant=True)
        conditions_true_5 = factories.LineEstimationTemplateConditionsFactory(
            condition_renewal_fee_from_filing_after_grant=True)
        conditions_false = factories.LineEstimationTemplateConditionsFactory(
            condition_renewal_fee_from_filing_after_grant=False)
        filing_est_template_cond_true = factories.FilingEstimateTemplateFactory(date_diff='P1Y',
                                                                                conditions=conditions_true)
        filing_est_template_cond_true_2 = factories.FilingEstimateTemplateFactory(date_diff='P2Y',
                                                                                  conditions=conditions_true_2)
        filing_est_template_cond_true_3 = factories.FilingEstimateTemplateFactory(date_diff='P3Y',
                                                                                  conditions=conditions_true_3)
        filing_est_template_cond_true_4 = factories.FilingEstimateTemplateFactory(date_diff='P4Y',
                                                                                  conditions=conditions_true_4)
        filing_est_template_cond_true_5 = factories.FilingEstimateTemplateFactory(date_diff='P5Y',
                                                                                  conditions=conditions_true_5)
        filing_est_template_false = factories.FilingEstimateTemplateFactory(date_diff='P1Y',
                                                                            conditions=conditions_false)

        total_date_diff = request_option.date_diff + oa_option.date_diff + allow_option.date_diff
        # P30M
        templates = FilingEstimateTemplate.objects.all()
        # filtered = utils._filter_renewal_fee_from_filing_after_grant(templates=templates, appl_option=appl_option)
        application = BaseUtilityApplicationFactory(date_filing=date(2010, 1, 1))
        publication = PublicationFactory(application=application, date_publication=date(2011, 6, 1))
        req_exam = RequestExaminationFactory(application=application, date_request_examination=date(2010, 6, 1))
        oa = OfficeActionFactory(application=application, date_office_action=date(2012, 1, 4))
        allowance = AllowanceFactory(application=application, date_allowance=date(2012, 9, 12))
        issuance = IssuanceFactory(application=application, date_issuance=date(2014, 5, 1))
        filtered = utils._filter_renewal_fee_from_filing_after_grant(templates=templates, application=application)
        self.assertEquals(filtered.count(), 2)
        self.assertIn(filing_est_template_cond_true_5, filtered)
        self.assertIn(filing_est_template_false, filtered)

    def test_utils_filter_prior_appl_pct_returns_only_false_and_none_condition(self):
        appl_option = ApplOptionsFactory()
        publ_option = PublOptionFactory(appl=appl_option, date_diff='P10M')
        request_option = RequestExaminationOptionFactory(appl=appl_option, date_diff='P10M')
        oa_option = OAOptionsFactory(appl=appl_option, date_diff='P10M')
        allow_option = AllowOptionsFactory(appl=appl_option, date_diff='P10M')
        issue_option = IssueOptionsFactory(appl=appl_option, date_diff='P10M')

        conditions_true = factories.LineEstimationTemplateConditionsFactory(
            prior_pct=True)
        conditions_true_2 = factories.LineEstimationTemplateConditionsFactory(
            prior_pct=True)
        conditions_true_3 = factories.LineEstimationTemplateConditionsFactory(
            prior_pct=True)
        conditions_false = factories.LineEstimationTemplateConditionsFactory(
            prior_pct=False)
        conditions_none = factories.LineEstimationTemplateConditionsFactory(
            prior_pct=None)
        filing_est_template_cond_true = factories.FilingEstimateTemplateFactory(date_diff='P1Y',
                                                                                conditions=conditions_true)
        filing_est_template_cond_true_2 = factories.FilingEstimateTemplateFactory(date_diff='P2Y',
                                                                                  conditions=conditions_true_2)
        filing_est_template_cond_true_3 = factories.FilingEstimateTemplateFactory(date_diff='P3Y',
                                                                                  conditions=conditions_true_3)
        filing_est_template_none = factories.FilingEstimateTemplateFactory(date_diff='P5Y',
                                                                           conditions=conditions_none)
        filing_est_template_false = factories.FilingEstimateTemplateFactory(date_diff='P1Y',
                                                                            conditions=conditions_false)

        total_date_diff = request_option.date_diff + oa_option.date_diff + allow_option.date_diff
        # P30M
        templates = FilingEstimateTemplate.objects.all()
        # filtered = utils._filter_renewal_fee_from_filing_after_grant(templates=templates, appl_option=appl_option)
        application = BaseUtilityApplicationFactory(date_filing=date(2015, 3, 5), prior_appl=None)
        filtered = utils._filter_prior_appl_pct(templates=templates, application=application)
        self.assertEquals(filtered.count(), 2)
        self.assertIn(filing_est_template_false, filtered)
        self.assertIn(filing_est_template_none, filtered)

    def test_utils_filter_prior_appl_pct_returns_only_false_and_none_condition_prior_appl_not_pct(self):
        appl_option = ApplOptionsFactory()
        appl_type_pct = ApplTypeFactory(pct=True)
        publ_option = PublOptionFactory(appl=appl_option, date_diff='P10M')
        request_option = RequestExaminationOptionFactory(appl=appl_option, date_diff='P10M')
        oa_option = OAOptionsFactory(appl=appl_option, date_diff='P10M')
        allow_option = AllowOptionsFactory(appl=appl_option, date_diff='P10M')
        issue_option = IssueOptionsFactory(appl=appl_option, date_diff='P10M')

        conditions_true = factories.LineEstimationTemplateConditionsFactory(
            prior_pct=True)
        conditions_true_2 = factories.LineEstimationTemplateConditionsFactory(
            prior_pct=True)
        conditions_true_3 = factories.LineEstimationTemplateConditionsFactory(
            prior_pct=True)
        conditions_false = factories.LineEstimationTemplateConditionsFactory(
            prior_pct=False)
        conditions_none = factories.LineEstimationTemplateConditionsFactory(
            prior_pct=None)
        filing_est_template_cond_true = factories.FilingEstimateTemplateFactory(date_diff='P1Y',
                                                                                conditions=conditions_true)
        filing_est_template_cond_true_2 = factories.FilingEstimateTemplateFactory(date_diff='P2Y',
                                                                                  conditions=conditions_true_2)
        filing_est_template_cond_true_3 = factories.FilingEstimateTemplateFactory(date_diff='P3Y',
                                                                                  conditions=conditions_true_3)
        filing_est_template_none = factories.FilingEstimateTemplateFactory(date_diff='P5Y',
                                                                           conditions=conditions_none)
        filing_est_template_false = factories.FilingEstimateTemplateFactory(date_diff='P1Y',
                                                                            conditions=conditions_false)

        total_date_diff = request_option.date_diff + oa_option.date_diff + allow_option.date_diff
        # P30M
        templates = FilingEstimateTemplate.objects.all()
        # filtered = utils._filter_renewal_fee_from_filing_after_grant(templates=templates, appl_option=appl_option)
        prior_application = BaseUtilityApplicationFactory(date_filing=date(2015, 3, 5), prior_appl=None)
        application = BaseUtilityApplicationFactory(date_filing=date(2015, 3, 5), prior_appl=prior_application)
        filtered = utils._filter_prior_appl_pct(templates=templates, application=application)
        self.assertEquals(filtered.count(), 2)
        self.assertIn(filing_est_template_false, filtered)
        self.assertIn(filing_est_template_none, filtered)

    def test_utils_filter_prior_appl_pct_returns_only_true_and_none_condition(self):
        appl_option = ApplOptionsFactory()
        appl_type_pct = ApplTypeFactory(pct=True)
        publ_option = PublOptionFactory(appl=appl_option, date_diff='P10M')
        request_option = RequestExaminationOptionFactory(appl=appl_option, date_diff='P10M')
        oa_option = OAOptionsFactory(appl=appl_option, date_diff='P10M')
        allow_option = AllowOptionsFactory(appl=appl_option, date_diff='P10M')
        issue_option = IssueOptionsFactory(appl=appl_option, date_diff='P10M')

        conditions_true = factories.LineEstimationTemplateConditionsFactory(
            prior_pct=True)
        conditions_true_2 = factories.LineEstimationTemplateConditionsFactory(
            prior_pct=True)
        conditions_true_3 = factories.LineEstimationTemplateConditionsFactory(
            prior_pct=True)
        conditions_false = factories.LineEstimationTemplateConditionsFactory(
            prior_pct=False)
        conditions_none = factories.LineEstimationTemplateConditionsFactory(
            prior_pct=None)
        filing_est_template_cond_true = factories.FilingEstimateTemplateFactory(date_diff='P1Y',
                                                                                conditions=conditions_true)
        filing_est_template_cond_true_2 = factories.FilingEstimateTemplateFactory(date_diff='P2Y',
                                                                                  conditions=conditions_true_2)
        filing_est_template_cond_true_3 = factories.FilingEstimateTemplateFactory(date_diff='P3Y',
                                                                                  conditions=conditions_true_3)
        filing_est_template_none = factories.FilingEstimateTemplateFactory(date_diff='P5Y',
                                                                           conditions=conditions_none)
        filing_est_template_false = factories.FilingEstimateTemplateFactory(date_diff='P1Y',
                                                                            conditions=conditions_false)

        total_date_diff = request_option.date_diff + oa_option.date_diff + allow_option.date_diff
        # P30M
        templates = FilingEstimateTemplate.objects.all()
        # filtered = utils._filter_renewal_fee_from_filing_after_grant(templates=templates, appl_option=appl_option)
        pct_application = PCTApplicationFactory(date_filing=date(2015, 3, 5), prior_appl=None)
        application = BaseUtilityApplicationFactory(date_filing=date(2015, 3, 5), prior_appl=pct_application)
        filtered = utils._filter_prior_appl_pct(templates=templates, application=application)
        self.assertEquals(filtered.count(), 4)
        self.assertIn(filing_est_template_cond_true, filtered)
        self.assertIn(filing_est_template_cond_true_2, filtered)
        self.assertIn(filing_est_template_cond_true_3, filtered)
        self.assertIn(filing_est_template_none, filtered)

    def test_utils_filter_prior_appl_pct_same_country_returns_only_false_and_none_condition(self):
        appl_option = ApplOptionsFactory()
        publ_option = PublOptionFactory(appl=appl_option, date_diff='P10M')
        request_option = RequestExaminationOptionFactory(appl=appl_option, date_diff='P10M')
        oa_option = OAOptionsFactory(appl=appl_option, date_diff='P10M')
        allow_option = AllowOptionsFactory(appl=appl_option, date_diff='P10M')
        issue_option = IssueOptionsFactory(appl=appl_option, date_diff='P10M')

        conditions_true = factories.LineEstimationTemplateConditionsFactory(
            prior_pct_same_country=True)
        conditions_true_2 = factories.LineEstimationTemplateConditionsFactory(
            prior_pct_same_country=True)
        conditions_true_3 = factories.LineEstimationTemplateConditionsFactory(
            prior_pct_same_country=True)
        conditions_false = factories.LineEstimationTemplateConditionsFactory(
            prior_pct_same_country=False)
        conditions_none = factories.LineEstimationTemplateConditionsFactory(
            prior_pct_same_country=None)
        filing_est_template_cond_true = factories.FilingEstimateTemplateFactory(date_diff='P1Y',
                                                                                conditions=conditions_true)
        filing_est_template_cond_true_2 = factories.FilingEstimateTemplateFactory(date_diff='P2Y',
                                                                                  conditions=conditions_true_2)
        filing_est_template_cond_true_3 = factories.FilingEstimateTemplateFactory(date_diff='P3Y',
                                                                                  conditions=conditions_true_3)
        filing_est_template_none = factories.FilingEstimateTemplateFactory(date_diff='P5Y',
                                                                           conditions=conditions_none)
        filing_est_template_false = factories.FilingEstimateTemplateFactory(date_diff='P1Y',
                                                                            conditions=conditions_false)

        total_date_diff = request_option.date_diff + oa_option.date_diff + allow_option.date_diff
        # P30M
        templates = FilingEstimateTemplate.objects.all()
        application = BaseUtilityApplicationFactory(date_filing=date(2015, 3, 5), prior_appl=None)
        filtered = utils._filter_prior_appl_pct_isa_same_country(templates=templates, application=application)
        self.assertEquals(filtered.count(), 2)
        self.assertIn(filing_est_template_false, filtered)
        self.assertIn(filing_est_template_none, filtered)

    def test_utils_filter_prior_appl_pct_same_country_returns_only_false_and_none_condition_not_pct(self):
        appl_option = ApplOptionsFactory()
        publ_option = PublOptionFactory(appl=appl_option, date_diff='P10M')
        request_option = RequestExaminationOptionFactory(appl=appl_option, date_diff='P10M')
        oa_option = OAOptionsFactory(appl=appl_option, date_diff='P10M')
        allow_option = AllowOptionsFactory(appl=appl_option, date_diff='P10M')
        issue_option = IssueOptionsFactory(appl=appl_option, date_diff='P10M')

        conditions_true = factories.LineEstimationTemplateConditionsFactory(
            prior_pct_same_country=True)
        conditions_true_2 = factories.LineEstimationTemplateConditionsFactory(
            prior_pct_same_country=True)
        conditions_true_3 = factories.LineEstimationTemplateConditionsFactory(
            prior_pct_same_country=True)
        conditions_false = factories.LineEstimationTemplateConditionsFactory(
            prior_pct_same_country=False)
        conditions_none = factories.LineEstimationTemplateConditionsFactory(
            prior_pct_same_country=None)
        filing_est_template_cond_true = factories.FilingEstimateTemplateFactory(date_diff='P1Y',
                                                                                conditions=conditions_true)
        filing_est_template_cond_true_2 = factories.FilingEstimateTemplateFactory(date_diff='P2Y',
                                                                                  conditions=conditions_true_2)
        filing_est_template_cond_true_3 = factories.FilingEstimateTemplateFactory(date_diff='P3Y',
                                                                                  conditions=conditions_true_3)
        filing_est_template_none = factories.FilingEstimateTemplateFactory(date_diff='P5Y',
                                                                           conditions=conditions_none)
        filing_est_template_false = factories.FilingEstimateTemplateFactory(date_diff='P1Y',
                                                                            conditions=conditions_false)

        total_date_diff = request_option.date_diff + oa_option.date_diff + allow_option.date_diff
        # P30M
        templates = FilingEstimateTemplate.objects.all()
        prior_application = BaseUtilityApplicationFactory(date_filing=date(2013, 3, 5), prior_appl=None)
        application = BaseUtilityApplicationFactory(date_filing=date(2015, 3, 5), prior_appl=prior_application)
        filtered = utils._filter_prior_appl_pct_isa_same_country(templates=templates, application=application)
        self.assertEquals(filtered.count(), 2)
        self.assertIn(filing_est_template_false, filtered)
        self.assertIn(filing_est_template_none, filtered)

    def test_utils_filter_prior_appl_pct_same_country_returns_only_false_and_none_conditions_diff_country(self):
        appl_option = ApplOptionsFactory()
        country_cn = CountryFactory(CN=True)
        country_us = CountryFactory(US=True)
        appl_type_pct = ApplTypeFactory(pct=True)
        publ_option = PublOptionFactory(appl=appl_option, date_diff='P10M')
        request_option = RequestExaminationOptionFactory(appl=appl_option, date_diff='P10M')
        oa_option = OAOptionsFactory(appl=appl_option, date_diff='P10M')
        allow_option = AllowOptionsFactory(appl=appl_option, date_diff='P10M')
        issue_option = IssueOptionsFactory(appl=appl_option, date_diff='P10M')

        conditions_true = factories.LineEstimationTemplateConditionsFactory(
            prior_pct_same_country=True)
        conditions_true_2 = factories.LineEstimationTemplateConditionsFactory(
            prior_pct_same_country=True)
        conditions_true_3 = factories.LineEstimationTemplateConditionsFactory(
            prior_pct_same_country=True)
        conditions_false = factories.LineEstimationTemplateConditionsFactory(
            prior_pct_same_country=False)
        conditions_none = factories.LineEstimationTemplateConditionsFactory(
            prior_pct_same_country=None)
        filing_est_template_cond_true = factories.FilingEstimateTemplateFactory(date_diff='P1Y',
                                                                                conditions=conditions_true)
        filing_est_template_cond_true_2 = factories.FilingEstimateTemplateFactory(date_diff='P2Y',
                                                                                  conditions=conditions_true_2)
        filing_est_template_cond_true_3 = factories.FilingEstimateTemplateFactory(date_diff='P3Y',
                                                                                  conditions=conditions_true_3)
        filing_est_template_none = factories.FilingEstimateTemplateFactory(date_diff='P5Y',
                                                                           conditions=conditions_none)
        filing_est_template_false = factories.FilingEstimateTemplateFactory(date_diff='P1Y',
                                                                            conditions=conditions_false)

        total_date_diff = request_option.date_diff + oa_option.date_diff + allow_option.date_diff
        # P30M
        templates = FilingEstimateTemplate.objects.all()
        prior_application = PCTApplicationFactory(date_filing=date(2013, 3, 5), prior_appl=None, isa_country=country_us)
        application = BaseUtilityApplicationFactory(date_filing=date(2015, 3, 5), prior_appl=prior_application,
                                                    country=country_cn)
        filtered = utils._filter_prior_appl_pct_isa_same_country(templates=templates, application=application)
        self.assertEquals(filtered.count(), 2)
        self.assertIn(filing_est_template_false, filtered)
        self.assertIn(filing_est_template_none, filtered)

    def test_utils_filter_prior_appl_pct_same_country_returns_only_true_and_none_conditions(self):
        appl_option = ApplOptionsFactory()
        country_cn = CountryFactory(CN=True)
        appl_type_pct = ApplTypeFactory(pct=True)
        publ_option = PublOptionFactory(appl=appl_option, date_diff='P10M')
        request_option = RequestExaminationOptionFactory(appl=appl_option, date_diff='P10M')
        oa_option = OAOptionsFactory(appl=appl_option, date_diff='P10M')
        allow_option = AllowOptionsFactory(appl=appl_option, date_diff='P10M')
        issue_option = IssueOptionsFactory(appl=appl_option, date_diff='P10M')

        conditions_true = factories.LineEstimationTemplateConditionsFactory(
            prior_pct_same_country=True)
        conditions_true_2 = factories.LineEstimationTemplateConditionsFactory(
            prior_pct_same_country=True)
        conditions_true_3 = factories.LineEstimationTemplateConditionsFactory(
            prior_pct_same_country=True)
        conditions_false = factories.LineEstimationTemplateConditionsFactory(
            prior_pct_same_country=False)
        conditions_none = factories.LineEstimationTemplateConditionsFactory(
            prior_pct_same_country=None)
        filing_est_template_cond_true = factories.FilingEstimateTemplateFactory(date_diff='P1Y',
                                                                                conditions=conditions_true)
        filing_est_template_cond_true_2 = factories.FilingEstimateTemplateFactory(date_diff='P2Y',
                                                                                  conditions=conditions_true_2)
        filing_est_template_cond_true_3 = factories.FilingEstimateTemplateFactory(date_diff='P3Y',
                                                                                  conditions=conditions_true_3)
        filing_est_template_none = factories.FilingEstimateTemplateFactory(date_diff='P5Y',
                                                                           conditions=conditions_none)
        filing_est_template_false = factories.FilingEstimateTemplateFactory(date_diff='P1Y',
                                                                            conditions=conditions_false)

        total_date_diff = request_option.date_diff + oa_option.date_diff + allow_option.date_diff
        # P30M
        templates = FilingEstimateTemplate.objects.all()
        prior_application = PCTApplicationFactory(date_filing=date(2013, 3, 5), prior_appl=None, isa_country=country_cn)
        application = BaseUtilityApplicationFactory(date_filing=date(2015, 3, 5), prior_appl=prior_application,
                                                    country=country_cn)
        filtered = utils._filter_prior_appl_pct_isa_same_country(templates=templates, application=application)
        self.assertEquals(filtered.count(), 4)
        self.assertIn(filing_est_template_cond_true, filtered)
        self.assertIn(filing_est_template_cond_true_2, filtered)
        self.assertIn(filing_est_template_cond_true_3, filtered)
        self.assertIn(filing_est_template_none, filtered)

    def test_utils_filter_prior_appl_filing_date_and_excluding_overlapping_dates_conditions_one_true(self):
        country_cn = CountryFactory(CN=True)
        appl_type_pct = ApplTypeFactory(pct=True)

        conditions_true = factories.LineEstimationTemplateConditionsFactory(
            prev_appl_date_excl_intermediary_time=True)
        conditions_true_2 = factories.LineEstimationTemplateConditionsFactory(
            prev_appl_date_excl_intermediary_time=True)
        conditions_true_3 = factories.LineEstimationTemplateConditionsFactory(
            prev_appl_date_excl_intermediary_time=True)
        conditions_false = factories.LineEstimationTemplateConditionsFactory(
            prev_appl_date_excl_intermediary_time=False)
        filing_est_template_cond_true = factories.FilingEstimateTemplateFactory(date_diff='P1Y',
                                                                                conditions=conditions_true)
        filing_est_template_cond_true_2 = factories.FilingEstimateTemplateFactory(date_diff='P2Y',
                                                                                  conditions=conditions_true_2)
        filing_est_template_cond_true_3 = factories.FilingEstimateTemplateFactory(date_diff='P3Y',
                                                                                  conditions=conditions_true_3)
        filing_est_template_false = factories.FilingEstimateTemplateFactory(date_diff='P1Y',
                                                                            conditions=conditions_false)

        # P30M
        templates = FilingEstimateTemplate.objects.all()
        prior_application = BaseUtilityApplicationFactory(date_filing=date(2013, 3, 5), prior_appl=None)
        application = BaseUtilityApplicationFactory(date_filing=date(2015, 3, 5), prior_appl=prior_application,
                                                    country=country_cn)
        filtered = utils._filter_fee_from_prior_appl_filing_date_and_excluding_overlapping_dates(templates=templates,
                                                                                                 application=application)
        self.assertEquals(filtered.count(), 2)
        self.assertIn(filing_est_template_cond_true_3, filtered)
        self.assertIn(filing_est_template_false, filtered)

    def test_utils_filter_prior_appl_filing_date_and_excluding_overlapping_dates_conditions_three_true(self):
        country_cn = CountryFactory(CN=True)
        appl_type_pct = ApplTypeFactory(pct=True)

        conditions_true = factories.LineEstimationTemplateConditionsFactory(
            prev_appl_date_excl_intermediary_time=True)
        conditions_true_2 = factories.LineEstimationTemplateConditionsFactory(
            prev_appl_date_excl_intermediary_time=True)
        conditions_true_3 = factories.LineEstimationTemplateConditionsFactory(
            prev_appl_date_excl_intermediary_time=True)
        conditions_true_4 = factories.LineEstimationTemplateConditionsFactory(
            prev_appl_date_excl_intermediary_time=True)
        conditions_false = factories.LineEstimationTemplateConditionsFactory(
            prev_appl_date_excl_intermediary_time=False)
        filing_est_template_cond_true = factories.FilingEstimateTemplateFactory(date_diff='P1Y',
                                                                                conditions=conditions_true)
        filing_est_template_cond_true_2 = factories.FilingEstimateTemplateFactory(date_diff='P2Y',
                                                                                  conditions=conditions_true_2)
        filing_est_template_cond_true_3 = factories.FilingEstimateTemplateFactory(date_diff='P3Y',
                                                                                  conditions=conditions_true_3)
        filing_est_template_cond_true_4 = factories.FilingEstimateTemplateFactory(date_diff='P4Y',
                                                                                  conditions=conditions_true_4)
        filing_est_template_false = factories.FilingEstimateTemplateFactory(date_diff='P1Y',
                                                                            conditions=conditions_false)

        # P30M
        templates = FilingEstimateTemplate.objects.all()
        prior_application = BaseUtilityApplicationFactory(date_filing=date(2013, 3, 5), prior_appl=None)
        application = BaseUtilityApplicationFactory(date_filing=date(2014, 4, 5), prior_appl=prior_application,
                                                    country=country_cn)
        filtered = utils._filter_fee_from_prior_appl_filing_date_and_excluding_overlapping_dates(templates=templates,
                                                                                                 application=application)
        self.assertEquals(filtered.count(), 4)
        self.assertIn(filing_est_template_cond_true_2, filtered)
        self.assertIn(filing_est_template_cond_true_3, filtered)
        self.assertIn(filing_est_template_cond_true_4, filtered)
        self.assertIn(filing_est_template_false, filtered)

    def test_utils_filter_fee_if_first_appl_returns_three_prior_appl(self):
        conditions_true = factories.LineEstimationTemplateConditionsFactory(
            prior_appl_exists=True)
        conditions_true_2 = factories.LineEstimationTemplateConditionsFactory(
            prior_appl_exists=True)
        conditions_false = factories.LineEstimationTemplateConditionsFactory(
            prior_appl_exists=False)
        conditions_none = factories.LineEstimationTemplateConditionsFactory(
            prior_appl_exists=None)
        filing_est_template_cond_true = factories.FilingEstimateTemplateFactory(date_diff='P1Y',
                                                                                conditions=conditions_true)
        filing_est_template_cond_true_2 = factories.FilingEstimateTemplateFactory(date_diff='P2Y',
                                                                                  conditions=conditions_true_2)
        filing_est_template_false = factories.FilingEstimateTemplateFactory(date_diff='P1Y',
                                                                            conditions=conditions_false)
        filing_est_template_none = factories.FilingEstimateTemplateFactory(date_diff='P1Y',
                                                                           conditions=conditions_none)

        templates = FilingEstimateTemplate.objects.all()
        prior_application = BaseUtilityApplicationFactory(date_filing=date(2013, 3, 5), prior_appl=None)
        application = BaseUtilityApplicationFactory(date_filing=date(2014, 4, 5), prior_appl=prior_application)
        filtered = utils._filter_fee_if_first_appl(templates=templates,
                                                   application=application)
        self.assertEquals(filtered.count(), 3)
        self.assertIn(filing_est_template_cond_true, filtered)
        self.assertIn(filing_est_template_cond_true_2, filtered)
        self.assertIn(filing_est_template_none, filtered)

    def test_utils_filter_fee_if_first_appl_returns_two_no_prior_appl(self):
        conditions_true = factories.LineEstimationTemplateConditionsFactory(
            prior_appl_exists=True)
        conditions_true_2 = factories.LineEstimationTemplateConditionsFactory(
            prior_appl_exists=True)
        conditions_false = factories.LineEstimationTemplateConditionsFactory(
            prior_appl_exists=False)
        conditions_none = factories.LineEstimationTemplateConditionsFactory(
            prior_appl_exists=None)
        filing_est_template_cond_true = factories.FilingEstimateTemplateFactory(date_diff='P1Y',
                                                                                conditions=conditions_true)
        filing_est_template_cond_true_2 = factories.FilingEstimateTemplateFactory(date_diff='P2Y',
                                                                                  conditions=conditions_true_2)
        filing_est_template_false = factories.FilingEstimateTemplateFactory(date_diff='P1Y',
                                                                            conditions=conditions_false)
        filing_est_template_none = factories.FilingEstimateTemplateFactory(date_diff='P1Y',
                                                                           conditions=conditions_none)

        templates = FilingEstimateTemplate.objects.all()
        prior_application = None
        application = BaseUtilityApplicationFactory(date_filing=date(2014, 4, 5), prior_appl=prior_application)
        filtered = utils._filter_fee_if_first_appl(templates=templates,
                                                   application=application)
        self.assertEquals(filtered.count(), 2)
        self.assertIn(filing_est_template_false, filtered)
        self.assertIn(filing_est_template_none, filtered)


class FilterConditionsTest(TestCase):

    def test_filter_conditions_test_case_1(self):
        appl_type_pct = ApplTypeFactory(pct=True)
        appl_type_nationalphase = ApplTypeFactory(nationalphase=True)
        appl_type_utility = ApplTypeFactory(utility=True)
        doc_format_electronic = DocFormatFactory(electronic=True)
        doc_format_paper = DocFormatFactory(paper=True)
        particulars = ApplOptionsParticularsFactory(doc_format=doc_format_electronic)
        entity_size_small = EntitySizeFactory(us_small=True)
        entity_size_micro = EntitySizeFactory(us_micro=True)
        language_cn = LanguageFactory(Chinese=True)
        language_en = LanguageFactory(English=True)
        country_cn = CountryFactory(CN=True)
        country_gb = CountryFactory(gb=True)

        appl_option = ApplOptionsFactory(particulars=particulars)
        details = ApplDetailsFactory(num_indep_claims=5,
                                     num_claims_multiple_dependent=5,
                                     num_pages_description=50,
                                     num_pages_claims=25,
                                     num_pages_drawings=25,
                                     num_claims=20,
                                     num_drawings=20,
                                     entity_size=entity_size_small,
                                     language=language_cn)
        priorapplication = PCTApplicationFactory(date_filing=date(1999, 1, 1), isa_country=country_gb)
        application = BaseUtilityApplicationFactory(
            country=country_cn,
            prior_appl=priorapplication,
            appl_option=appl_option,
            details=details,
            date_filing=date(2000, 1, 1))
        allowance = AllowanceFactory(application=application, date_allowance=date(2001, 1, 1))
        issue = IssuanceFactory(application=application, date_issuance=date(2002, 2, 1))
        conditions_claims_min_pass = factories.LineEstimationTemplateConditionsFactory(
            condition_claims_min=10)
        template_claims_min_pass = factories.FilingEstimateTemplateFactory(date_diff='P1Y',
                                                                           conditions=conditions_claims_min_pass)
        conditions_claims_min_fail = factories.LineEstimationTemplateConditionsFactory(
            condition_claims_min=25)
        template_claims_min_fail = factories.FilingEstimateTemplateFactory(date_diff='P1Y',
                                                                           conditions=conditions_claims_min_fail)
        # ****************************
        conditions_claims_max_pass = factories.LineEstimationTemplateConditionsFactory(
            condition_claims_max=25)
        template_claims_max_pass = factories.FilingEstimateTemplateFactory(date_diff='P1Y',
                                                                           conditions=conditions_claims_max_pass)
        conditions_claims_max_fail = factories.LineEstimationTemplateConditionsFactory(
            condition_claims_max=10)
        template_claims_max_fail = factories.FilingEstimateTemplateFactory(date_diff='P1Y',
                                                                           conditions=conditions_claims_max_fail)

        # ****************************
        conditions_indep_claims_min_pass = factories.LineEstimationTemplateConditionsFactory(
            condition_indep_claims_min=2)
        template_indep_claims_min_pass = factories.FilingEstimateTemplateFactory(date_diff='P1Y',
                                                                                 conditions=conditions_indep_claims_min_pass)
        conditions_indep_claims_min_fail = factories.LineEstimationTemplateConditionsFactory(
            condition_indep_claims_min=10)
        template_indep_claims_min_fail = factories.FilingEstimateTemplateFactory(date_diff='P1Y',
                                                                                 conditions=conditions_indep_claims_min_fail)
        conditions_indep_claims_max_pass = factories.LineEstimationTemplateConditionsFactory(
            condition_indep_claims_max=10)
        template_indep_claims_max_pass = factories.FilingEstimateTemplateFactory(date_diff='P1Y',
                                                                                 conditions=conditions_indep_claims_max_pass)
        conditions_indep_claims_max_fail = factories.LineEstimationTemplateConditionsFactory(
            condition_indep_claims_max=3)
        template_indep_claims_max_fail = factories.FilingEstimateTemplateFactory(date_diff='P1Y',
                                                                                 conditions=conditions_indep_claims_max_fail)

        # ****************************
        conditions_claims_multiple_dependent_min_pass = factories.LineEstimationTemplateConditionsFactory(
            condition_claims_multiple_dependent_min=2)
        template_claims_multiple_dependent_min_pass = factories.FilingEstimateTemplateFactory(date_diff='P1Y',
                                                                                              conditions=conditions_claims_multiple_dependent_min_pass)
        conditions_claims_multiple_dependent_min_fail = factories.LineEstimationTemplateConditionsFactory(
            condition_claims_multiple_dependent_min=25)
        template_claims_multiple_dependent_min_fail = factories.FilingEstimateTemplateFactory(date_diff='P1Y',
                                                                                              conditions=conditions_claims_multiple_dependent_min_fail)
        conditions_claims_multiple_dependent_max_pass = factories.LineEstimationTemplateConditionsFactory(
            condition_claims_multiple_dependent_max=10)
        template_claims_multiple_dependent_max_pass = factories.FilingEstimateTemplateFactory(date_diff='P1Y',
                                                                                              conditions=conditions_claims_multiple_dependent_max_pass)
        conditions_claims_multiple_dependent_max_fail = factories.LineEstimationTemplateConditionsFactory(
            condition_claims_multiple_dependent_max=3)
        template_claims_multiple_dependent_max_fail = factories.FilingEstimateTemplateFactory(date_diff='P1Y',
                                                                                              conditions=conditions_claims_multiple_dependent_max_fail)

        conditions_pages_total_min_pass = factories.LineEstimationTemplateConditionsFactory(
            condition_pages_total_min=100)
        template_pages_total_min_pass = factories.FilingEstimateTemplateFactory(date_diff='P1Y',
                                                                                conditions=conditions_pages_total_min_pass)
        conditions_pages_total_min_fail = factories.LineEstimationTemplateConditionsFactory(
            condition_pages_total_min=101)
        template_pages_total_min_fail = factories.FilingEstimateTemplateFactory(date_diff='P1Y',
                                                                                conditions=conditions_pages_total_min_fail)
        # ****************************
        conditions_pages_total_max_pass = factories.LineEstimationTemplateConditionsFactory(
            condition_pages_total_max=100)
        template_pages_total_max_pass = factories.FilingEstimateTemplateFactory(date_diff='P1Y',
                                                                                conditions=conditions_pages_total_max_pass)
        conditions_pages_total_max_fail = factories.LineEstimationTemplateConditionsFactory(
            condition_pages_total_max=99)
        template_pages_total_max_fail = factories.FilingEstimateTemplateFactory(date_diff='P1Y',
                                                                                conditions=conditions_pages_total_max_fail)

        # ****************************
        conditions_pages_description_min_pass = factories.LineEstimationTemplateConditionsFactory(
            condition_pages_desc_min=50)
        template_pages_description_min_pass = factories.FilingEstimateTemplateFactory(date_diff='P1Y',
                                                                                      conditions=conditions_pages_description_min_pass)
        conditions_pages_description_min_fail = factories.LineEstimationTemplateConditionsFactory(
            condition_pages_desc_min=51)
        template_pages_description_min_fail = factories.FilingEstimateTemplateFactory(date_diff='P1Y',
                                                                                      conditions=conditions_pages_description_min_fail)
        conditions_pages_description_max_pass = factories.LineEstimationTemplateConditionsFactory(
            condition_pages_desc_max=50)
        template_pages_description_max_pass = factories.FilingEstimateTemplateFactory(date_diff='P1Y',
                                                                                      conditions=conditions_pages_description_max_pass)
        conditions_pages_description_max_fail = factories.LineEstimationTemplateConditionsFactory(
            condition_pages_desc_max=49)
        template_pages_description_max_fail = factories.FilingEstimateTemplateFactory(date_diff='P1Y',
                                                                                      conditions=conditions_pages_description_max_fail)

        # ****************************
        conditions_pages_claims_min_pass = factories.LineEstimationTemplateConditionsFactory(
            condition_pages_claims_min=25)
        template_pages_claims_min_pass = factories.FilingEstimateTemplateFactory(date_diff='P1Y',
                                                                                 conditions=conditions_pages_claims_min_pass)
        conditions_pages_claims_min_fail = factories.LineEstimationTemplateConditionsFactory(
            condition_pages_claims_min=26)
        template_pages_claims_min_fail = factories.FilingEstimateTemplateFactory(date_diff='P1Y',
                                                                                 conditions=conditions_pages_claims_min_fail)
        conditions_pages_claims_max_pass = factories.LineEstimationTemplateConditionsFactory(
            condition_pages_claims_max=25)
        template_pages_claims_max_pass = factories.FilingEstimateTemplateFactory(date_diff='P1Y',
                                                                                 conditions=conditions_pages_claims_max_pass)
        conditions_pages_claims_max_fail = factories.LineEstimationTemplateConditionsFactory(
            condition_pages_claims_max=24)
        template_pages_claims_max_fail = factories.FilingEstimateTemplateFactory(date_diff='P1Y',
                                                                                 conditions=conditions_pages_claims_max_fail)

        # ****************************
        conditions_pages_drawings_min_pass = factories.LineEstimationTemplateConditionsFactory(
            condition_pages_drawings_min=25)
        template_pages_drawings_min_pass = factories.FilingEstimateTemplateFactory(date_diff='P1Y',
                                                                                   conditions=conditions_pages_drawings_min_pass)
        conditions_pages_drawings_min_fail = factories.LineEstimationTemplateConditionsFactory(
            condition_pages_drawings_min=26)
        template_pages_drawings_min_fail = factories.FilingEstimateTemplateFactory(date_diff='P1Y',
                                                                                   conditions=conditions_pages_drawings_min_fail)
        conditions_pages_drawings_max_pass = factories.LineEstimationTemplateConditionsFactory(
            condition_pages_drawings_max=25)
        template_pages_drawings_max_pass = factories.FilingEstimateTemplateFactory(date_diff='P1Y',
                                                                                   conditions=conditions_pages_drawings_max_pass)
        conditions_pages_drawings_max_fail = factories.LineEstimationTemplateConditionsFactory(
            condition_pages_drawings_max=24)
        template_pages_drawings_max_fail = factories.FilingEstimateTemplateFactory(date_diff='P1Y',
                                                                                   conditions=conditions_pages_drawings_max_fail)

        # ****************************
        conditions_drawings_min_pass = factories.LineEstimationTemplateConditionsFactory(
            condition_drawings_min=20)
        template_drawings_min_pass = factories.FilingEstimateTemplateFactory(date_diff='P1Y',
                                                                             conditions=conditions_drawings_min_pass)
        conditions_drawings_min_fail = factories.LineEstimationTemplateConditionsFactory(
            condition_drawings_min=21)
        template_drawings_min_fail = factories.FilingEstimateTemplateFactory(date_diff='P1Y',
                                                                             conditions=conditions_drawings_min_fail)
        conditions_drawings_max_pass = factories.LineEstimationTemplateConditionsFactory(
            condition_drawings_max=20)
        template_drawings_max_pass = factories.FilingEstimateTemplateFactory(date_diff='P1Y',
                                                                             conditions=conditions_drawings_max_pass)
        conditions_drawings_max_fail = factories.LineEstimationTemplateConditionsFactory(
            condition_drawings_max=19)
        template_drawings_max_fail = factories.FilingEstimateTemplateFactory(date_diff='P1Y',
                                                                             conditions=conditions_drawings_max_fail)

        # ****************************
        conditions_entity_size_pass = factories.LineEstimationTemplateConditionsFactory(
            condition_entity_size=entity_size_small)
        template_entity_size_pass = factories.FilingEstimateTemplateFactory(date_diff='P1Y',
                                                                            conditions=conditions_entity_size_pass)
        conditions_entity_size_fail = factories.LineEstimationTemplateConditionsFactory(
            condition_entity_size=entity_size_micro)
        template_entity_size_fail = factories.FilingEstimateTemplateFactory(date_diff='P1Y',
                                                                            conditions=conditions_entity_size_fail)

        # ****************************
        conditions_language_pass = factories.LineEstimationTemplateConditionsFactory(
            language=language_cn)
        template_language_pass = factories.FilingEstimateTemplateFactory(date_diff='P1Y',
                                                                         conditions=conditions_language_pass)
        conditions_language_fail = factories.LineEstimationTemplateConditionsFactory(
            language=language_en)
        template_language_fail = factories.FilingEstimateTemplateFactory(date_diff='P1Y',
                                                                         conditions=conditions_language_fail)

        # ****************************
        conditions_doc_format_pass = factories.LineEstimationTemplateConditionsFactory(
            doc_format=doc_format_electronic)
        template_doc_format_pass = factories.FilingEstimateTemplateFactory(date_diff='P1Y',
                                                                           conditions=conditions_doc_format_pass)
        conditions_doc_format_fail = factories.LineEstimationTemplateConditionsFactory(
            doc_format=doc_format_paper)
        template_doc_format_fail = factories.FilingEstimateTemplateFactory(date_diff='P1Y',
                                                                           conditions=conditions_doc_format_fail)

        conditions_annual_prosecution_fee_pass = factories.LineEstimationTemplateConditionsFactory(
            condition_annual_prosecution_fee=True)
        template_annual_prosecution_pass = factories.FilingEstimateTemplateFactory(date_diff='P1Y',
                                                                                   conditions=conditions_annual_prosecution_fee_pass)
        conditions_annual_prosecution_fee_fail = factories.LineEstimationTemplateConditionsFactory(
            condition_annual_prosecution_fee=True)
        template_annual_prosecution_fail = factories.FilingEstimateTemplateFactory(date_diff='P2Y',
                                                                                   conditions=conditions_annual_prosecution_fee_fail)

        conditions_annual_prosecution_fee_until_grant_pass = factories.LineEstimationTemplateConditionsFactory(
            condition_annual_prosecution_fee_until_grant=True)
        template_annual_prosecution_until_grant_pass = factories.FilingEstimateTemplateFactory(date_diff='P2Y',
                                                                                               conditions=conditions_annual_prosecution_fee_until_grant_pass)
        conditions_annual_prosecution_fee_until_grant_fail = factories.LineEstimationTemplateConditionsFactory(
            condition_annual_prosecution_fee_until_grant=True)
        template_annual_prosecution_until_grant_fail = factories.FilingEstimateTemplateFactory(date_diff='P3Y',
                                                                                               conditions=conditions_annual_prosecution_fee_until_grant_fail)

        conditions_renewal_fee_from_filing_after_grant_pass = factories.LineEstimationTemplateConditionsFactory(
            condition_renewal_fee_from_filing_after_grant=True)
        template_renewal_fee_from_filing_after_grant_pass = factories.FilingEstimateTemplateFactory(date_diff='P3Y',
                                                                                                    conditions=conditions_renewal_fee_from_filing_after_grant_pass)
        conditions_renewal_fee_from_filing_after_grant_fail = factories.LineEstimationTemplateConditionsFactory(
            condition_renewal_fee_from_filing_after_grant=True)
        template_renewal_fee_from_filing_after_grant_fail = factories.FilingEstimateTemplateFactory(date_diff='P2Y',
                                                                                                    conditions=conditions_renewal_fee_from_filing_after_grant_fail)

        conditions_prior_pct_pass = factories.LineEstimationTemplateConditionsFactory(
            prior_pct=True)
        template_prior_pct_pass = factories.FilingEstimateTemplateFactory(
            date_diff='P3Y',
            conditions=conditions_prior_pct_pass)
        conditions_prior_pct_fail = factories.LineEstimationTemplateConditionsFactory(
            prior_pct=False)
        template_prior_pct_fail = factories.FilingEstimateTemplateFactory(
            date_diff='P2Y',
            conditions=conditions_prior_pct_fail)

        conditions_prior_pct_isa_pass = factories.LineEstimationTemplateConditionsFactory(
            prior_pct_same_country=False)
        template_prior_pct_isa_pass = factories.FilingEstimateTemplateFactory(
            date_diff='P2Y',
            conditions=conditions_prior_pct_isa_pass)
        conditions_prior_pct_isa_fail = factories.LineEstimationTemplateConditionsFactory(
            prior_pct_same_country=True)
        template_prior_pct_isa_fail = factories.FilingEstimateTemplateFactory(
            date_diff='P2Y',
            conditions=conditions_prior_pct_isa_fail)

        conditions_prev_appl_date_excl_intermediary_time_pass = factories.LineEstimationTemplateConditionsFactory(
            prev_appl_date_excl_intermediary_time=True)
        template_prev_appl_date_excl_intermediary_time_pass = factories.FilingEstimateTemplateFactory(
            date_diff='P2Y',
            conditions=conditions_prev_appl_date_excl_intermediary_time_pass)
        conditions_prev_appl_date_excl_intermediary_time_fail = factories.LineEstimationTemplateConditionsFactory(
            prev_appl_date_excl_intermediary_time=True)
        template_prev_appl_date_excl_intermediary_time_fail = factories.FilingEstimateTemplateFactory(
            date_diff='P1Y',
            conditions=conditions_prev_appl_date_excl_intermediary_time_fail)

        conditions_prior_appl_exists_pass = factories.LineEstimationTemplateConditionsFactory(
            prior_appl_exists=True)
        template_prior_appl_exists_pass = factories.FilingEstimateTemplateFactory(
            date_diff='P2Y',
            conditions=conditions_prior_appl_exists_pass)
        conditions_prior_appl_exists_fail = factories.LineEstimationTemplateConditionsFactory(
            prior_appl_exists=False)
        template_prior_appl_exists_fail = factories.FilingEstimateTemplateFactory(
            date_diff='P2Y',
            conditions=conditions_prior_appl_exists_fail)

        country_cn = CountryFactory(CN=True, currency_name='CNY')
        country_us = CountryFactory(US=True, currency_name='USD')
        conditions_isa_country_fee_only_fail_CNY = factories.LineEstimationTemplateConditionsFactory(
            isa_country_fee_only=True)
        filing_est_template_fail_CNY = factories.FilingEstimateTemplateFactory(
            conditions=conditions_isa_country_fee_only_fail_CNY,
            official_cost=Money(100, 'CNY'))
        conditions_isa_country_fee_only_fail_USD = factories.LineEstimationTemplateConditionsFactory(
            isa_country_fee_only=True)
        filing_est_template_fail_USD = factories.FilingEstimateTemplateFactory(
            conditions=conditions_isa_country_fee_only_fail_USD,
            official_cost=Money(40, 'USD'))

        templates = FilingEstimateTemplate.objects.all()
        filtered = utils.filter_conditions(templates=templates, application=application)

        self.assertIn(template_claims_min_pass, filtered)
        self.assertNotIn(template_claims_min_fail, filtered)
        self.assertIn(template_claims_max_pass, filtered)
        self.assertNotIn(template_claims_max_fail, filtered)

        self.assertIn(template_indep_claims_min_pass, filtered)
        self.assertNotIn(template_indep_claims_min_fail, filtered)
        self.assertIn(template_indep_claims_max_pass, filtered)
        self.assertNotIn(template_indep_claims_max_fail, filtered)

        self.assertIn(template_claims_multiple_dependent_min_pass, filtered)
        self.assertNotIn(template_claims_multiple_dependent_min_fail, filtered)
        self.assertIn(template_claims_multiple_dependent_max_pass, filtered)
        self.assertNotIn(template_claims_multiple_dependent_max_fail, filtered)

        self.assertIn(template_pages_total_min_pass, filtered)
        self.assertNotIn(template_pages_total_min_fail, filtered)
        self.assertIn(template_pages_total_max_pass, filtered)
        self.assertNotIn(template_pages_total_max_fail, filtered)

        self.assertIn(template_pages_description_min_pass, filtered)
        self.assertNotIn(template_pages_description_min_fail, filtered)
        self.assertIn(template_pages_description_max_pass, filtered)
        self.assertNotIn(template_pages_description_max_fail, filtered)

        self.assertIn(template_pages_claims_min_pass, filtered)
        self.assertNotIn(template_pages_claims_min_fail, filtered)
        self.assertIn(template_pages_claims_max_pass, filtered)
        self.assertNotIn(template_pages_claims_max_fail, filtered)

        self.assertIn(template_pages_drawings_min_pass, filtered)
        self.assertNotIn(template_pages_drawings_min_fail, filtered)
        self.assertIn(template_pages_drawings_max_pass, filtered)
        self.assertNotIn(template_pages_drawings_max_fail, filtered)

        self.assertIn(template_drawings_min_pass, filtered)
        self.assertNotIn(template_drawings_min_fail, filtered)
        self.assertIn(template_drawings_max_pass, filtered)
        self.assertNotIn(template_drawings_max_fail, filtered)

        self.assertIn(template_entity_size_pass, filtered)
        self.assertNotIn(template_entity_size_fail, filtered)

        self.assertIn(template_language_pass, filtered)
        self.assertNotIn(template_language_fail, filtered)

        self.assertIn(template_doc_format_pass, filtered)
        self.assertNotIn(template_doc_format_fail, filtered)

        self.assertIn(template_annual_prosecution_pass, filtered)
        self.assertNotIn(template_annual_prosecution_fail, filtered)

        self.assertIn(template_annual_prosecution_until_grant_pass, filtered)
        self.assertNotIn(template_annual_prosecution_until_grant_fail, filtered)

        self.assertIn(template_renewal_fee_from_filing_after_grant_pass, filtered)
        self.assertNotIn(template_renewal_fee_from_filing_after_grant_fail, filtered)

        self.assertIn(template_prior_pct_pass, filtered)
        self.assertNotIn(template_prior_pct_fail, filtered)

        self.assertIn(template_prior_pct_isa_pass, filtered)
        self.assertNotIn(template_prior_pct_isa_fail, filtered)

        self.assertIn(template_prev_appl_date_excl_intermediary_time_pass, filtered)
        self.assertNotIn(template_prev_appl_date_excl_intermediary_time_fail, filtered)

        self.assertIn(template_prior_pct_pass, filtered)
        self.assertNotIn(template_prior_pct_fail, filtered)

        self.assertNotIn(filing_est_template_fail_CNY, filtered)
        self.assertNotIn(filing_est_template_fail_USD, filtered)
