from datetime import datetime
from math import trunc

from django.db.models import Sum
from django.test import TestCase
from djmoney.contrib.exchange.models import convert_money
from djmoney.money import Money

from characteristics.factories import ApplTypeFactory, CountryFactory, EntitySizeFactory
from estimation.factories import FilingEstimateTemplateFactory, PublicationEstTemplateFactory, \
    OAEstimateTemplateFactory, AllowanceEstTemplateFactory, IssueEstTemplateFactory, USOAEstimateTemplateFactory, \
    LineEstimationTemplateConditionsFactory
from estimation.models import \
    OAEstimate, OAEstimateTemplate, \
    PublicationEstTemplate, \
    PublicationEst, AllowanceEst, IssueEst, USOAEstimateTemplate, \
    USOAEstimate, FilingEstimate, LawFirmEst, LawFirmEstTemplate, IssueEstTemplate, AllowanceEstTemplate, \
    FilingEstimateTemplate
from famform.factories import ApplOptionsFactory, PCTApplOptionsFactory, PublOptionFactory, AllowOptionsFactory, \
    OAOptionsFactory, \
    IssueOptionsFactory, RequestExaminationOptionFactory, USOAOptionsFactory
from famform.models import OAOptions, RequestExaminationOptions
from famform.models.USOAOptions import USOAOptions
from family.factories import FamilyFactory
from transform.factories import DefaultFilingTransformFactory, CustomFilingTransformFactory, IssueTransformFactory, \
    AllowanceTransformFactory, OATransformFactory, PublicationTransformFactory, CountryOANumFactory, \
    DefaultCountryOANumFactory, DefaultPublTransformFactory, DefaultOATransformFactory, \
    DefaultAllowanceTransformFactory, DefaultIssueTransformFactory, RequestExaminationTransformFactory
from user.factories import UserFactory
from .factories import USUtilityApplicationFactory, USOfficeActionFactory, IssuanceFactory, \
    AllowanceFactory, PublicationFactory, BaseUtilityApplicationFactory, OfficeActionFactory, ApplDetailsFactory
from .models import BaseApplication, OfficeAction, PCTApplication
from .models.allowance import Allowance
from .models.issue import Issue
from .models.publication import Publication
from .models.usOfficeAction import USOfficeAction
from .models.baseUtilityApplication import BaseUtilityApplication


# Create your tests here.
class PCTApplicationTest(TestCase):

    def setUp(self):
        self.user = UserFactory()
        self.applType_prov = ApplTypeFactory(prov=True)
        self.applType_pct = ApplTypeFactory(pct=True)
        # self.applType_utility = ApplTypeFactory(utility=True)
        self.country_US = CountryFactory(US=True)
        self.country_CN = CountryFactory(CN=True)
        self.country_JP = CountryFactory(country='JP')
        self.countries = [self.country_US, self.country_CN]
        self.entitySize = EntitySizeFactory()
        self.family = FamilyFactory(user=self.user)

        self.dfltFilTrans_prov = DefaultFilingTransformFactory(appl_type=self.applType_prov)
        self.dfltFilTrans_pct = DefaultFilingTransformFactory(appl_type=self.applType_pct)
        self.defaultCountryOANum = DefaultCountryOANumFactory()
        self.dfltPublTrans_pct = DefaultPublTransformFactory(appl_type=self.applType_pct)
        self.dfltOATrans = DefaultOATransformFactory(appl_type=self.applType_pct)
        self.allowTrans = DefaultAllowanceTransformFactory(appl_type=self.applType_pct)
        self.IssueTrans = DefaultIssueTransformFactory(appl_type=self.applType_pct)

        self.customFilTrans = CustomFilingTransformFactory(appl_type=self.applType_prov,
                                                           prev_appl_type=None,
                                                           country=self.country_US)
        self.issTrans = IssueTransformFactory(country=self.country_US)
        self.allowTrans = AllowanceTransformFactory(country=self.country_US)
        self.requestExamTrans = RequestExaminationTransformFactory(country=self.country_US)
        self.oaTrans = OATransformFactory(country=self.country_US)
        self.publTrans = PublicationTransformFactory(country=self.country_US, appl_type=self.applType_pct)
        self.countryOANum = CountryOANumFactory(country=self.country_US)

        self.filing_template_us = FilingEstimateTemplateFactory(country=self.country_US,
                                                                appl_type=self.applType_pct)
        self.publication_template = PublicationEstTemplateFactory(country=self.country_US, appl_type=self.applType_pct)
        self.oa_template_jp = OAEstimateTemplateFactory(country=self.country_JP)
        self.oa_template_cn = OAEstimateTemplateFactory(country=self.country_CN)
        self.oa_template_us = USOAEstimateTemplateFactory(appl_type=self.applType_pct)
        self.allowance_template = AllowanceEstTemplateFactory(country=self.country_US)
        self.issue_template = IssueEstTemplateFactory(country=self.country_US)

        self.applOption = PCTApplOptionsFactory(country=self.country_US, appl_type=self.applType_pct)
        self.publOption = PublOptionFactory(appl=self.applOption)
        self.reqExamOption = RequestExaminationOptionFactory(appl=self.applOption)
        self.oaOption = OAOptionsFactory(appl=self.applOption)
        self.allowOption = AllowOptionsFactory(appl=self.applOption)
        self.issueOption = IssueOptionsFactory(appl=self.applOption)

    def test_create_full_creates_Publication(self):
        PCTApplication.objects.create_full(options=self.applOption,
                                           user=self.user,
                                           family_id=self.family.id)

        uAppl = BaseApplication.objects.get(user=self.user)
        date_publication = uAppl.date_filing + self.publOption.date_diff
        self.assertEquals(date_publication, Publication.objects.first().date_publication)

    # def test_create_full_creates_oa(self):
    #     PCTApplication.objects.create_full(options=self.applOption,
    #                                        user=self.user,
    #                                        family_id=self.family.id)
    #
    #     uAppl = BaseApplication.objects.get(user=self.user)
    #     req_diff = self.reqExamOption.date_diff
    #     # relativedelta is calced by combining options in Setup
    #     date_allowance = uAppl.date_filing + req_diff + self.oaOption.date_diff
    #     self.assertEquals(date_allowance, OfficeAction.objects.first().date_office_action)

    def test_generate_filing_est(self):
        PCTApplication.objects.create_full(options=self.applOption,
                                           user=self.user,
                                           family_id=self.family.id)
        uAppl = BaseApplication.objects.get(user=self.user)
        self.assertEquals(FilingEstimate.objects.get(application=uAppl).official_cost,
                          FilingEstimateTemplate.objects.first().official_cost)

    def test_create_full_publication_est(self):
        PCTApplication.objects.create_full(options=self.applOption,
                                           user=self.user, family_id=self.family.id)
        publEstTemp = PublicationEstTemplate.objects.all()
        self.assertEquals(PublicationEstTemplate.objects.first().official_cost,
                          PublicationEst.objects.all().first().official_cost)

    # def test_create_full_oa_est(self):
    #     UtilityApplication.objects.create_full(options=self.applOption,
    #                                            user=self.user, family_id=self.family.id)
    #     self.assertEquals(USOAEstimateTemplate.objects.first().official_cost,
    #                       USOAEstimate.objects.all().first().official_cost
    #                       )
    #
    # def test_create_full_oa_est_cn(self):
    #     applOption = ApplOptionsFactory(country=self.country_CN, appl_type=self.applType_pct)
    #     publOption = PublOptionFactory(appl=applOption)
    #     reqExamOption = RequestExaminationOptionFactory(appl=applOption)
    #     oaOption = OAOptionsFactory(appl=applOption)
    #     allowOption = AllowOptionsFactory(appl=applOption)
    #     issueOption = IssueOptionsFactory(appl=applOption)
    #
    #     UtilityApplication.objects.create_full(options=applOption,
    #                                            user=self.user, family_id=self.family.id)
    #
    #     self.assertEquals(OAEstimateTemplate.objects.filter(country=self.country_CN).first().official_cost,
    #                       OAEstimate.objects.all().first().official_cost
    #                       )

    # def test_create_full_allowance_est(self):
    #     UtilityApplication.objects.create_full(options=self.applOption,
    #                                            user=self.user, family_id=self.family.id)
    #     self.assertEquals(AllowanceEstTemplate.objects.first().official_cost,
    #                       AllowanceEst.objects.all().first().official_cost
    #                       )
    #
    # def test_create_full_issue_est(self):
    #     UtilityApplication.objects.create_full(options=self.applOption,
    #                                            user=self.user, family_id=self.family.id)
    #     self.assertEquals(IssueEstTemplate.objects.first().official_cost,
    #                       IssueEst.objects.all().first().official_cost
    #                       )
    #
    # def test_create_ordered_oa_creates_ordered_array(self):
    #     application = USUtilityApplicationFactory(country=self.country_CN)
    #     applOption = ApplOptionsFactory(country=self.country_CN, appl_type=self.applType_pct)
    #     oaOption_one = OAOptionsFactory(appl=applOption, oa_prev=None)
    #     oaOption_two = OAOptionsFactory(appl=applOption, oa_prev=oaOption_one)
    #     oaOption_three = OAOptionsFactory(appl=applOption, oa_prev=oaOption_two)
    #     oaOption_four = OAOptionsFactory(appl=applOption, oa_prev=oaOption_three)
    #     oas_in = OAOptions.objects.filter(appl=applOption)
    #     ordered_oa = application._create_ordered_oa(oas_in=oas_in)
    #     self.assertEquals(oaOption_one, ordered_oa[0])
    #     self.assertEquals(oaOption_two, ordered_oa[1])
    #     self.assertEquals(oaOption_three, ordered_oa[2])
    #     self.assertEquals(oaOption_four, ordered_oa[3])
    #
    # def test_oa_dates_calculated(self):
    #     application = BaseUtilityApplicationFactory(country=self.country_CN)
    #     req_options = RequestExaminationOptions.objects.get(appl=self.applOption)
    #     applOption = ApplOptionsFactory(country=self.country_CN, appl_type=self.applType_pct)
    #     oaOption_one = OAOptionsFactory(appl=applOption, oa_prev=None)
    #     oaOption_two = OAOptionsFactory(appl=applOption, oa_prev=oaOption_one)
    #     oaOption_three = OAOptionsFactory(appl=applOption, oa_prev=oaOption_two)
    #     oaOption_four = OAOptionsFactory(appl=applOption, oa_prev=oaOption_three)
    #     oa_options = OAOptions.objects.filter(appl=applOption)
    #     date_request_examination = application.date_filing + req_options.date_diff
    #     application._generate_oa(date_request_examination=date_request_examination, oas_in=oa_options)
    #     oas = OfficeAction.objects.filter(application=application)
    #     oa_first = [x for x in oas if x.oa_prev is None][0]
    #     oa_option_first = [y for y in oa_options if y.oa_prev is None][0]
    #     self.assertEquals(oa_first.date_office_action,
    #                       (oa_option_first.date_diff + application.date_filing + req_options.date_diff))
    #
    #     oa_second = [x for x in oas if x.oa_prev == oa_first][0]
    #     oa_option_second = [y for y in oa_options if y.oa_prev == oa_option_first][0]
    #     self.assertEquals(oa_second.date_office_action,
    #                       (oa_option_second.date_diff + oa_first.date_office_action))
    #     oa_third = [x for x in oas if x.oa_prev == oa_second][0]
    #     oa_option_third = [y for y in oa_options if y.oa_prev == oa_option_second][0]
    #     self.assertEquals(oa_third.date_office_action,
    #                       (oa_option_third.date_diff + oa_second.date_office_action))
    #     oa_fourth = [x for x in oas if x.oa_prev == oa_third][0]
    #     oa_option_fourth = [y for y in oa_options if y.oa_prev == oa_option_third][0]
    #     self.assertEquals(oa_fourth.date_office_action,
    #                       (oa_option_fourth.date_diff + oa_third.date_office_action))


class BaseUtilityApplicationTest(TestCase):

    def setUp(self):
        self.user = UserFactory()
        self.applType_prov = ApplTypeFactory(prov=True)
        self.applType_pct = ApplTypeFactory(pct=True)
        self.applType_utility = ApplTypeFactory(utility=True)
        self.country_US = CountryFactory(US=True)
        self.country_CN = CountryFactory(CN=True)
        self.country_JP = CountryFactory(country='JP')
        self.countries = [self.country_US, self.country_CN]
        self.entitySize = EntitySizeFactory()
        self.family = FamilyFactory(user=self.user)

        self.dfltFilTrans_prov = DefaultFilingTransformFactory(appl_type=self.applType_prov)
        self.dfltFilTrans_pct = DefaultFilingTransformFactory(appl_type=self.applType_pct)
        self.dfltFilTrans_utility = DefaultFilingTransformFactory(appl_type=self.applType_utility)
        self.defaultCountryOANum = DefaultCountryOANumFactory()
        self.dfltPublTrans_pct = DefaultPublTransformFactory(appl_type=self.applType_pct)
        self.dfltPublTrans_utility = DefaultPublTransformFactory(appl_type=self.applType_utility)
        self.dfltOATrans = DefaultOATransformFactory(appl_type=self.applType_utility)
        self.allowTrans = DefaultAllowanceTransformFactory(appl_type=self.applType_utility)
        self.IssueTrans = DefaultIssueTransformFactory(appl_type=self.applType_utility)

        self.customFilTrans = CustomFilingTransformFactory(appl_type=self.applType_prov,
                                                           prev_appl_type=None,
                                                           country=self.country_US)
        self.issTrans = IssueTransformFactory(country=self.country_US)
        self.allowTrans = AllowanceTransformFactory(country=self.country_US)
        self.requestExamTrans = RequestExaminationTransformFactory(country=self.country_US)
        self.oaTrans = OATransformFactory(country=self.country_US)
        self.publTrans = PublicationTransformFactory(country=self.country_US)
        self.countryOANum = CountryOANumFactory(country=self.country_US)

        self.filing_template_us = FilingEstimateTemplateFactory(country=self.country_US,
                                                                appl_type=self.applType_utility)
        self.publication_template = PublicationEstTemplateFactory(country=self.country_US)
        self.oa_template_jp = OAEstimateTemplateFactory(country=self.country_JP)
        self.oa_template_cn = OAEstimateTemplateFactory(country=self.country_CN)
        self.oa_template_us = USOAEstimateTemplateFactory()
        self.allowance_template = AllowanceEstTemplateFactory(country=self.country_US)
        self.issue_template = IssueEstTemplateFactory(country=self.country_US)

        self.applOption = ApplOptionsFactory(country=self.country_US, appl_type=self.applType_utility)
        self.publOption = PublOptionFactory(appl=self.applOption)
        self.reqExamOption = RequestExaminationOptionFactory(appl=self.applOption)
        self.oaOption = OAOptionsFactory(appl=self.applOption)
        self.usOaOption = USOAOptionsFactory(appl=self.applOption)
        self.allowOption = AllowOptionsFactory(appl=self.applOption)
        self.issueOption = IssueOptionsFactory(appl=self.applOption)

    def test_create_full_creates_Publication(self):
        BaseUtilityApplication.objects.create_full(options=self.applOption,
                                                   user=self.user,
                                                   family_id=self.family.id)

        uAppl = BaseApplication.objects.get(user=self.user)
        date_publication = uAppl.date_filing + self.publOption.date_diff
        self.assertEquals(date_publication, Publication.objects.first().date_publication)

    def test_create_full_creates_oa(self):
        BaseUtilityApplication.objects.create_full(options=self.applOption,
                                                   user=self.user,
                                                   family_id=self.family.id)

        uAppl = BaseApplication.objects.get(user=self.user)
        req_diff = self.reqExamOption.date_diff
        # relativedelta is calced by combining options in Setup
        date_allowance = uAppl.date_filing + req_diff + self.usOaOption.date_diff
        self.assertEquals(date_allowance, USOfficeAction.objects.first().date_office_action)

    def test_create_full_creates_allowance(self):
        BaseUtilityApplication.objects.create_full(options=self.applOption,
                                                   user=self.user,
                                                   family_id=self.family.id)
        uAppl = BaseApplication.objects.get(user=self.user)
        # relativedelta is calced by combining options in Setup
        req_diff = self.reqExamOption.date_diff
        oa_agg = USOAOptions.objects.filter(appl=self.applOption).aggregate(date_diff=Sum('date_diff'))
        allow_diff = self.applOption.allowoptions.date_diff
        date_allowance = uAppl.date_filing + req_diff + oa_agg['date_diff'] + allow_diff
        self.assertEquals(date_allowance, Allowance.objects.first().date_allowance)

    def test_create_full_creates_issue(self):
        BaseUtilityApplication.objects.create_full(options=self.applOption,
                                                   user=self.user,
                                                   family_id=self.family.id)
        uAppl = BaseApplication.objects.get(user=self.user)
        req_diff = self.reqExamOption.date_diff
        oa_agg = USOAOptions.objects.filter(appl=self.applOption).aggregate(date_diff=Sum('date_diff'))
        allow_diff = self.applOption.allowoptions.date_diff
        issue_diff = self.applOption.issueoptions.date_diff
        date_issuance = uAppl.date_filing + req_diff + oa_agg['date_diff'] + allow_diff + issue_diff
        self.assertEquals(date_issuance, Issue.objects.first().date_issuance)

    def test_generate_filing_est(self):
        BaseUtilityApplication.objects.create_full(options=self.applOption,
                                                   user=self.user,
                                                   family_id=self.family.id)
        uAppl = BaseApplication.objects.get(user=self.user)
        self.assertEquals(FilingEstimate.objects.get(application=uAppl).official_cost,
                          FilingEstimateTemplate.objects.first().official_cost)

    def test_create_full_publication_est(self):
        BaseUtilityApplication.objects.create_full(options=self.applOption,
                                                   user=self.user, family_id=self.family.id)
        publEstTemp = PublicationEstTemplate.objects.all()
        self.assertEquals(PublicationEstTemplate.objects.first().official_cost,
                          PublicationEst.objects.all().first().official_cost
                          )

    def test_create_full_oa_est(self):
        BaseUtilityApplication.objects.create_full(options=self.applOption,
                                                   user=self.user, family_id=self.family.id)
        self.assertEquals(USOAEstimateTemplate.objects.first().official_cost,
                          USOAEstimate.objects.all().first().official_cost
                          )

    def test_create_full_oa_est_cn(self):
        applOption = ApplOptionsFactory(country=self.country_CN, appl_type=self.applType_utility)
        publOption = PublOptionFactory(appl=applOption)
        reqExamOption = RequestExaminationOptionFactory(appl=applOption)
        oaOption = OAOptionsFactory(appl=applOption)
        usoaOption = USOAOptionsFactory(appl=applOption)
        allowOption = AllowOptionsFactory(appl=applOption)
        issueOption = IssueOptionsFactory(appl=applOption)

        BaseUtilityApplication.objects.create_full(options=applOption,
                                                   user=self.user, family_id=self.family.id)

        self.assertEquals(OAEstimateTemplate.objects.filter(country=self.country_CN).first().official_cost,
                          OAEstimate.objects.all().first().official_cost
                          )

    def test_create_full_allowance_est(self):
        BaseUtilityApplication.objects.create_full(options=self.applOption,
                                                   user=self.user, family_id=self.family.id)
        self.assertEquals(AllowanceEstTemplate.objects.first().official_cost,
                          AllowanceEst.objects.all().first().official_cost
                          )

    def test_create_full_issue_est(self):
        BaseUtilityApplication.objects.create_full(options=self.applOption,
                                                   user=self.user, family_id=self.family.id)
        self.assertEquals(IssueEstTemplate.objects.first().official_cost,
                          IssueEst.objects.all().first().official_cost
                          )

    def test_create_ordered_oa_creates_ordered_array(self):
        application = USUtilityApplicationFactory(country=self.country_CN)
        applOption = ApplOptionsFactory(country=self.country_CN, appl_type=self.applType_utility)
        oaOption_one = OAOptionsFactory(appl=applOption, oa_prev=None)
        oaOption_two = OAOptionsFactory(appl=applOption, oa_prev=oaOption_one)
        oaOption_three = OAOptionsFactory(appl=applOption, oa_prev=oaOption_two)
        oaOption_four = OAOptionsFactory(appl=applOption, oa_prev=oaOption_three)
        oas_in = OAOptions.objects.filter(appl=applOption)
        ordered_oa = application._create_ordered_oa(oas_in=oas_in)
        self.assertEquals(oaOption_one, ordered_oa[0])
        self.assertEquals(oaOption_two, ordered_oa[1])
        self.assertEquals(oaOption_three, ordered_oa[2])
        self.assertEquals(oaOption_four, ordered_oa[3])

    def test_oa_dates_calculated(self):
        application = BaseUtilityApplicationFactory(country=self.country_CN)
        req_options = RequestExaminationOptions.objects.get(appl=self.applOption)
        applOption = ApplOptionsFactory(country=self.country_CN, appl_type=self.applType_utility)
        oaOption_one = OAOptionsFactory(appl=applOption, oa_prev=None)
        oaOption_two = OAOptionsFactory(appl=applOption, oa_prev=oaOption_one)
        oaOption_three = OAOptionsFactory(appl=applOption, oa_prev=oaOption_two)
        oaOption_four = OAOptionsFactory(appl=applOption, oa_prev=oaOption_three)
        oa_options = OAOptions.objects.filter(appl=applOption)
        date_request_examination = application.date_filing + req_options.date_diff
        application._generate_oa(date_request_examination=date_request_examination, oas_in=oa_options)
        oas = OfficeAction.objects.filter(application=application)
        oa_first = [x for x in oas if x.oa_prev is None][0]
        oa_option_first = [y for y in oa_options if y.oa_prev is None][0]
        self.assertEquals(oa_first.date_office_action,
                          (oa_option_first.date_diff + application.date_filing + req_options.date_diff))

        oa_second = [x for x in oas if x.oa_prev == oa_first][0]
        oa_option_second = [y for y in oa_options if y.oa_prev == oa_option_first][0]
        self.assertEquals(oa_second.date_office_action,
                          (oa_option_second.date_diff + oa_first.date_office_action))
        oa_third = [x for x in oas if x.oa_prev == oa_second][0]
        oa_option_third = [y for y in oa_options if y.oa_prev == oa_option_second][0]
        self.assertEquals(oa_third.date_office_action,
                          (oa_option_third.date_diff + oa_second.date_office_action))
        oa_fourth = [x for x in oas if x.oa_prev == oa_third][0]
        oa_option_fourth = [y for y in oa_options if y.oa_prev == oa_option_third][0]
        self.assertEquals(oa_fourth.date_office_action,
                          (oa_option_fourth.date_diff + oa_third.date_office_action))


#
#     # def test_generate_oa_adds_oa_estimate_templates(self):


class USUtilityApplicationTest(TestCase):

    def setUp(self):
        self.user = UserFactory()
        self.applType_prov = ApplTypeFactory(prov=True)
        self.applType_pct = ApplTypeFactory(pct=True)
        self.applType_utility = ApplTypeFactory(utility=True)
        self.country_US = CountryFactory(US=True)
        self.countries = [self.country_US]
        self.entitySize = EntitySizeFactory()
        self.family = FamilyFactory(user=self.user)

        self.dfltFilTrans_prov = DefaultFilingTransformFactory(appl_type=self.applType_prov)
        self.dfltFilTrans_pct = DefaultFilingTransformFactory(appl_type=self.applType_pct)
        self.dfltFilTrans_utility = DefaultFilingTransformFactory(appl_type=self.applType_utility)
        self.defaultCountryOANum = DefaultCountryOANumFactory()
        self.dfltPublTrans_pct = DefaultPublTransformFactory(appl_type=self.applType_pct)
        self.dfltPublTrans_utility = DefaultPublTransformFactory(appl_type=self.applType_utility)
        self.requestExamTrans = RequestExaminationTransformFactory(country=self.country_US)
        self.dfltOATrans = DefaultOATransformFactory(appl_type=self.applType_utility)
        self.allowTrans = DefaultAllowanceTransformFactory(appl_type=self.applType_utility)
        self.IssueTrans = DefaultIssueTransformFactory(appl_type=self.applType_utility)

        self.customFilTrans = CustomFilingTransformFactory(appl_type=self.applType_prov,
                                                           prev_appl_type=None,
                                                           country=self.country_US)
        self.issTrans = IssueTransformFactory(country=self.country_US)
        self.allowTrans = AllowanceTransformFactory(country=self.country_US)
        self.oaTrans = OATransformFactory(country=self.country_US)
        self.publTrans = PublicationTransformFactory(country=self.country_US)
        self.countryOANum = CountryOANumFactory(country=self.country_US, oa_total=3)

        self.filing_template_us = FilingEstimateTemplateFactory(country=self.country_US,
                                                                appl_type=self.applType_utility)
        self.publication_template = PublicationEstTemplateFactory(country=self.country_US,
                                                                  appl_type=self.applType_utility)
        self.oa_template = USOAEstimateTemplateFactory(appl_type=self.applType_utility)
        self.oa_template_foa = USOAEstimateTemplateFactory(first_foa=True, appl_type=self.applType_utility)
        self.allowance_template = AllowanceEstTemplateFactory(country=self.country_US, appl_type=self.applType_utility)
        self.issue_template = IssueEstTemplateFactory(country=self.country_US, appl_type=self.applType_utility)

        self.applOption = ApplOptionsFactory(country=self.country_US, appl_type=self.applType_utility)
        self.pre_applOption = ApplOptionsFactory(country=self.country_US, appl_type=self.applType_utility)
        self.publOption = PublOptionFactory(appl=self.applOption)
        self.reqExamOption = RequestExaminationOptionFactory(appl=self.applOption)
        self.pre_oaOption = USOAOptionsFactory(appl=self.pre_applOption)
        self.oaOption = USOAOptionsFactory(appl=self.applOption, oa_final_bool=False)
        self.oaOption_two = USOAOptionsFactory(appl=self.applOption, oa_prev=self.oaOption, oa_final_bool=True)
        self.oaOption_three = USOAOptionsFactory(appl=self.applOption, oa_prev=self.oaOption_two, oa_final_bool=False)
        self.oaOption_four = USOAOptionsFactory(appl=self.applOption, oa_prev=self.oaOption_three, oa_final_bool=True)
        self.allowOption = AllowOptionsFactory(appl=self.applOption)
        self.issueOption = IssueOptionsFactory(appl=self.applOption)

    def test_creates_only_one_primary_oas(self):
        application = USUtilityApplicationFactory(country=self.country_US)
        req_options = RequestExaminationOptions.objects.get(appl=self.applOption)
        oa_options = USOAOptions.objects.filter(appl=self.applOption)
        date_request_examination = application.date_filing + req_options.date_diff
        application._generate_oa(date_request_examination=date_request_examination, oas_in=oa_options)
        oas = USOfficeAction.objects.all()
        self.assertTrue(oas.filter(oa_prev=None).count() == 1)

    def test_create_ordered_oa_creates_ordered_array(self):
        application = USUtilityApplicationFactory(country=self.country_US)
        applOption = ApplOptionsFactory(country=self.country_US, appl_type=self.applType_utility)
        oaOption_one = USOAOptionsFactory(appl=applOption, oa_prev=None)
        oaOption_two = USOAOptionsFactory(appl=applOption, oa_prev=oaOption_one)
        oaOption_three = USOAOptionsFactory(appl=applOption, oa_prev=oaOption_two)
        oaOption_four = USOAOptionsFactory(appl=applOption, oa_prev=oaOption_three)
        oas_in = USOAOptions.objects.filter(appl=applOption)
        ordered_oa = application._create_ordered_oa(oas_in=oas_in)
        self.assertEquals(oaOption_one, ordered_oa[0])
        self.assertEquals(oaOption_two, ordered_oa[1])
        self.assertEquals(oaOption_three, ordered_oa[2])
        self.assertEquals(oaOption_four, ordered_oa[3])

    def test_create_multiple_oas_nfoa_foa_nfoa_foa(self):
        application = USUtilityApplicationFactory(country=self.country_US)
        oa_options = USOAOptions.objects.filter(appl=self.applOption)
        req_options = RequestExaminationOptions.objects.get(appl=self.applOption)
        date_request_examination = application.date_filing + req_options.date_diff
        application._generate_oa(date_request_examination=date_request_examination, oas_in=oa_options)
        oas = USOfficeAction.objects.all()
        self.assertTrue(oas.filter(oa_prev=None).count() == 1)
        oa_first = [x for x in oas if x.oa_prev is None]
        self.assertFalse(oa_first[0].oa_final_bool)
        oa_second = [x for x in oas if x.oa_prev == oa_first[0]]
        self.assertTrue(oa_second[0].oa_final_bool)
        oa_third = [x for x in oas if x.oa_prev == oa_second[0]]
        self.assertFalse(oa_third[0].oa_final_bool)
        oa_fourth = [x for x in oas if x.oa_prev == oa_third[0]]
        self.assertTrue(oa_fourth[0].oa_final_bool)

    def test_oa_dates_calculated(self):
        application = USUtilityApplicationFactory(country=self.country_US)
        req_options = RequestExaminationOptions.objects.get(appl=self.applOption)
        oa_options = USOAOptions.objects.filter(appl=self.applOption)
        date_request_examination = application.date_filing + req_options.date_diff
        application._generate_oa(date_request_examination=date_request_examination, oas_in=oa_options)
        oas = USOfficeAction.objects.all()

        oa_first = [x for x in oas if x.oa_prev is None][0]
        oa_option_first = [y for y in oa_options if y.oa_prev_id is None][0]
        self.assertEquals(oa_first.date_office_action,
                          (oa_option_first.date_diff + application.date_filing + req_options.date_diff))
        oa_second = [x for x in oas if x.oa_prev_id == oa_first.id][0]
        oa_option_second = [y for y in oa_options if y.oa_prev_id == oa_option_first.id][0]
        self.assertEquals(oa_second.date_office_action,
                          (oa_option_second.date_diff + oa_first.date_office_action))
        oa_third = [x for x in oas if x.oa_prev_id == oa_second.id][0]
        oa_option_third = [y for y in oa_options if y.oa_prev_id == oa_option_second.id][0]
        self.assertEquals(oa_third.date_office_action,
                          (oa_option_third.date_diff + oa_second.date_office_action))
        oa_fourth = [x for x in oas if x.oa_prev_id == oa_third.id][0]
        oa_option_fourth = [y for y in oa_options if y.oa_prev_id == oa_option_third.id][0]
        self.assertEquals(oa_fourth.date_office_action,
                          (oa_option_fourth.date_diff + oa_third.date_office_action))


class AllowanceTest(TestCase):

    def setUp(self):
        self.country_us = CountryFactory(US=True)
        self.applType_prov = ApplTypeFactory(prov=True)
        self.applType_pct = ApplTypeFactory(pct=True)
        self.applType_utility = ApplTypeFactory(utility=True)
        self.entity_size = EntitySizeFactory(us_small=True)
        self.details = ApplDetailsFactory(entity_size=self.entity_size)
        self.application = USUtilityApplicationFactory(country=self.country_us, details=self.details,
                                                       date_filing=datetime(2020, 10, 1).date())
        self.usAllowance = AllowanceFactory(application=self.application)
        self.conditions_one = LineEstimationTemplateConditionsFactory(
            condition_entity_size=EntitySizeFactory(us_small=True))
        self.conditions_two = LineEstimationTemplateConditionsFactory(
            condition_entity_size=EntitySizeFactory(us_small=True))
        self.conditions_three = LineEstimationTemplateConditionsFactory(
            condition_entity_size=EntitySizeFactory(us_small=True))
        self.allowEstTemp_one = AllowanceEstTemplateFactory(country=self.country_us,
                                                            conditions=self.conditions_one,
                                                            appl_type=self.applType_utility)
        self.allowEstTemp_two = AllowanceEstTemplateFactory(country=self.country_us,
                                                            conditions=self.conditions_two,
                                                            appl_type=self.applType_utility)

        self.allowEStTemp_three = AllowanceEstTemplateFactory(country=self.country_us,
                                                              conditions=self.conditions_three,
                                                              appl_type=self.applType_utility)

    def test_generate_ests_creates_three_ests(self):
        self.usAllowance.generate_ests()
        self.assertEquals(AllowanceEst.objects.all().count(), 3)
        self.assertEquals(AllowanceEstTemplate.objects.all().count(),
                          AllowanceEst.objects.all().count())

    def test_generate_ests_creates_correct_cost(self):
        self.usAllowance.generate_ests()
        self.assertEquals(AllowanceEstTemplate.objects.all().aggregate(Sum('official_cost')),
                          AllowanceEst.objects.all().aggregate(Sum('official_cost')))

    def test_generate_ests_creates_three_law_firm_ests(self):
        self.usAllowance.generate_ests()
        self.assertEquals(AllowanceEst.objects.all().count(), 3)
        self.assertEquals(AllowanceEstTemplate.objects.all().count(),
                          AllowanceEst.objects.all().count())

    def test_generate_ests_creates_correct_cost_law_firm_ests(self):
        self.usAllowance.generate_ests()
        self.assertEquals(LawFirmEstTemplate.objects.all().aggregate(Sum('law_firm_cost')),
                          LawFirmEst.objects.all().aggregate(Sum('law_firm_cost')))

    def test_generate_ests_creates_3_of_4_ests(self):
        conditions = LineEstimationTemplateConditionsFactory(condition_entity_size=EntitySizeFactory(micro=True))
        AllowanceEstTemplateFactory.create(country=self.country_us,
                                           appl_type=self.applType_utility,
                                           conditions=conditions)
        self.usAllowance.generate_ests()
        self.assertEquals(AllowanceEstTemplate.objects.all().count(), 4)
        self.assertEquals(AllowanceEst.objects.all().count(), 3)

    def test_generate_ests_creates_correct_date(self):
        # conditions = LineEstimationTemplateConditionsFactory(condition_entity_size=EntitySizeFactory(small=True))
        # allowEstTemp = AllowanceEstTemplateFactory.create(country=self.country_us,
        #                                appl_type=self.applType_utility,
        #                                conditions=self.conditions)
        entitySize = EntitySizeFactory(small=True)
        application = USUtilityApplicationFactory(country=self.country_us,
                                                  details=ApplDetailsFactory(entity_size=entitySize))
        # usAllow = AllowanceFactory(application=application)
        # usAllow.generate_ests()
        self.usAllowance.generate_ests()
        self.assertEquals(AllowanceEst.objects.all().first().date,
                          self.allowEstTemp_one.date_diff + self.usAllowance.date_allowance)


class IssueTest(TestCase):

    def setUp(self):
        self.country_us = CountryFactory(US=True)
        self.applType_prov = ApplTypeFactory(prov=True)
        self.applType_pct = ApplTypeFactory(pct=True)
        self.applType_utility = ApplTypeFactory(utility=True)
        self.entity_size = EntitySizeFactory(us_small=True)
        self.details = ApplDetailsFactory(entity_size=self.entity_size)
        self.application = USUtilityApplicationFactory(country=self.country_us, details=self.details,
                                                       date_filing=datetime(2020, 10, 1).date())
        self.usIssuance = IssuanceFactory(application=self.application)

        self.conditions_one = LineEstimationTemplateConditionsFactory(
            condition_entity_size=EntitySizeFactory(us_small=True))
        self.conditions_two = LineEstimationTemplateConditionsFactory(
            condition_entity_size=EntitySizeFactory(us_small=True))
        self.conditions_three = LineEstimationTemplateConditionsFactory(
            condition_entity_size=EntitySizeFactory(us_small=True))

        self.issueEstTemp_one = IssueEstTemplateFactory(country=self.country_us,
                                                        conditions=self.conditions_one,
                                                        appl_type=self.applType_utility)
        self.issueEstTemp_two = IssueEstTemplateFactory(country=self.country_us,
                                                        conditions=self.conditions_two,
                                                        appl_type=self.applType_utility)

        self.issueEstTemp_three = IssueEstTemplateFactory(country=self.country_us,
                                                          conditions=self.conditions_three,
                                                          appl_type=self.applType_utility)

    def test_generate_ests_creates_three_ests(self):
        self.usIssuance.generate_ests()
        self.assertEquals(IssueEstTemplate.objects.all().count(), 3)
        self.assertEquals(IssueEstTemplate.objects.all().count(),
                          IssueEst.objects.all().count())

    def test_generate_ests_creates_correct_cost(self):
        self.usIssuance.generate_ests()
        self.assertEquals(IssueEstTemplate.objects.all().aggregate(Sum('official_cost')),
                          IssueEst.objects.all().aggregate(Sum('official_cost')))

    def test_generate_ests_creates_correct_cost_law_firm_ests(self):
        self.usIssuance.generate_ests()
        self.assertEquals(LawFirmEstTemplate.objects.all().aggregate(Sum('law_firm_cost')),
                          LawFirmEst.objects.all().aggregate(Sum('law_firm_cost')))

    def test_generate_ests_creates_three_law_firm_ests(self):
        self.usIssuance.generate_ests()
        self.assertEquals(IssueEst.objects.all().count(), 3)
        self.assertEquals(IssueEstTemplate.objects.all().count(),
                          IssueEst.objects.all().count())

    def test_generate_ests_creates_3_of_4_ests(self):
        conditions = LineEstimationTemplateConditionsFactory(condition_entity_size=EntitySizeFactory(micro=True))
        IssueEstTemplateFactory.create(country=self.country_us,
                                       appl_type=self.applType_utility,
                                       conditions=conditions)
        self.usIssuance.generate_ests()
        self.assertEquals(IssueEstTemplate.objects.all().count(), 4)
        self.assertEquals(IssueEst.objects.all().count(), 3)

    def test_generate_ests_creates_correct_date(self):
        # conditions = LineEstimationTemplateConditionsFactory(condition_entity_size=EntitySizeFactory(small=True))
        # issueEstTemp = IssueEstTemplateFactory.create(country=self.country_us,
        #                                      appl_type=self.applType_utility,
        #                                      conditions=conditions)
        # entitySize = EntitySizeFactory(small=True)
        # application = USUtilityApplicationFactory(country=self.country_us,
        #                                           details=ApplDetailsFactory(entity_size=entitySize))
        # usIssue = IssuanceFactory(application=application)
        # usIssue.generate_ests()
        self.usIssuance.generate_ests()
        self.assertEquals(IssueEst.objects.all().first().date,
                          self.issueEstTemp_one.date_diff + self.usIssuance.date_issuance)


class OfficeActionTest(TestCase):
    fixtures = ['exchange-data.json']

    def setUp(self):
        self.country_cn = CountryFactory(CN=True)
        self.applType_prov = ApplTypeFactory(prov=True)
        self.applType_pct = ApplTypeFactory(pct=True)
        self.applType_utility = ApplTypeFactory(utility=True)
        self.entity_size = EntitySizeFactory(us_small=True)
        self.details = ApplDetailsFactory(entity_size=self.entity_size)
        self.application = BaseUtilityApplicationFactory(country=self.country_cn, details=self.details,
                                                         date_filing=datetime(2020, 10, 1).date())
        self.cnOfficeAction = OfficeActionFactory(application=self.application)

        self.conditions_one = LineEstimationTemplateConditionsFactory(
            condition_entity_size=EntitySizeFactory(us_small=True))
        self.conditions_two = LineEstimationTemplateConditionsFactory(
            condition_entity_size=EntitySizeFactory(us_small=True))
        self.conditions_three = LineEstimationTemplateConditionsFactory(
            condition_entity_size=EntitySizeFactory(us_small=True))

        self.oaEstTemplate_one = OAEstimateTemplateFactory(
            CN=True,
            conditions=self.conditions_one,
            appl_type=self.applType_utility)
        self.oaEstTemplate_two = OAEstimateTemplateFactory(
            CN=True,
            conditions=self.conditions_two,
            appl_type=self.applType_utility)
        self.oaEstTemplate_three = OAEstimateTemplateFactory(
            CN=True,
            conditions=self.conditions_three,
            appl_type=self.applType_utility)

    def test_generate_ests_creates_three_ests(self):
        self.cnOfficeAction.generate_ests()
        self.assertEquals(OAEstimateTemplate.objects.all().count(), 3)
        self.assertEquals(OAEstimateTemplate.objects.all().count(),
                          OAEstimate.objects.all().count())

    def test_generate_ests_creates_correct_cost(self):
        self.cnOfficeAction.generate_ests()
        oaEstTemps_tot = OAEstimateTemplate.objects.all().aggregate((Sum('official_cost')))
        self.assertEquals(trunc(convert_money(Money(oaEstTemps_tot['official_cost__sum'], 'CNY'), 'USD').amount),
                          trunc(OAEstimate.objects.all().aggregate(Sum('official_cost'))['official_cost__sum']))

    def test_generate_ests_creates_three_law_firm_ests(self):
        self.cnOfficeAction.generate_ests()
        self.assertEquals(LawFirmEst.objects.all().count(), 3)
        self.assertEquals(LawFirmEstTemplate.objects.all().count(),
                          LawFirmEst.objects.all().count())

    def test_generate_ests_creates_correct_cost_law_firm_ests(self):
        self.cnOfficeAction.generate_ests()
        law_est_temps_tot = LawFirmEstTemplate.objects.all().aggregate(Sum('law_firm_cost'))
        self.assertEquals(trunc(convert_money(Money(law_est_temps_tot['law_firm_cost__sum'], 'CNY'), 'USD').amount),
                          trunc(LawFirmEst.objects.all().aggregate(Sum('law_firm_cost'))['law_firm_cost__sum']))

    def test_generate_ests_creates_3_of_4_ests(self):
        conditions = LineEstimationTemplateConditionsFactory(condition_entity_size=EntitySizeFactory(micro=True))
        OAEstimateTemplateFactory.create(country=self.country_cn,
                                         appl_type=self.applType_utility,
                                         conditions=conditions)
        self.cnOfficeAction.generate_ests()
        self.assertEquals(OAEstimateTemplate.objects.all().count(), 4)
        self.assertEquals(OAEstimate.objects.all().count(), 3)

    def test_generate_ests_creates_correct_date(self):
        # conditions = LineEstimationTemplateConditionsFactory(condition_entity_size=EntitySizeFactory(small=True))
        # OAEstimateTemplateFactory.create(country=self.country_cn,
        #                                  appl_type=self.applType_utility,
        #                                  conditions=conditions)
        # entitySize = EntitySizeFactory(small=True)
        # BaseUtilityApplicationFactory(country=self.country_cn,
        #                                             details=ApplDetailsFactory(entity_size=entitySize))
        # cnOfficeAction = OfficeActionFactory(application=self.application)
        self.cnOfficeAction.generate_ests()
        self.assertEquals(OAEstimate.objects.all().first().date,
                          self.oaEstTemplate_one.date_diff + self.cnOfficeAction.date_office_action)


class USOfficeActionTest(TestCase):
    fixtures = ['exchange-data.json']

    def setUp(self):
        self.country_us = CountryFactory(US=True)
        self.applType_prov = ApplTypeFactory(prov=True)
        self.applType_pct = ApplTypeFactory(pct=True)
        self.applType_utility = ApplTypeFactory(utility=True)
        self.entity_size = EntitySizeFactory(us_small=True)
        self.details = ApplDetailsFactory(entity_size=self.entity_size)
        self.application = USUtilityApplicationFactory(country=self.country_us, details=self.details,
                                                       date_filing=datetime(2020, 10, 1).date())
        self.usOfficeAction = USOfficeActionFactory(application=self.application)

        self.conditions_one = LineEstimationTemplateConditionsFactory(
            condition_entity_size=EntitySizeFactory(us_small=True))
        self.conditions_two = LineEstimationTemplateConditionsFactory(
            condition_entity_size=EntitySizeFactory(us_small=True))
        self.conditions_three = LineEstimationTemplateConditionsFactory(
            condition_entity_size=EntitySizeFactory(us_small=True))
        self.usOAEstTemplate_one = USOAEstimateTemplateFactory(country=self.country_us,
                                                               conditions=self.conditions_one,
                                                               appl_type=self.applType_utility)
        self.usOAEstTemplate_two = USOAEstimateTemplateFactory(country=self.country_us,
                                                               conditions=self.conditions_two,
                                                               appl_type=self.applType_utility)
        self.usOAEstTemplate_three = USOAEstimateTemplateFactory(country=self.country_us,
                                                                 conditions=self.conditions_three,
                                                                 appl_type=self.applType_utility)

    def test_generate_ests_creates_three_ests(self):
        self.usOfficeAction.generate_ests()
        self.assertEquals(USOAEstimateTemplate.objects.all().count(), 3)
        self.assertEquals(USOAEstimateTemplate.objects.all().count(),
                          USOAEstimate.objects.all().count())

    def test_generate_ests_creates_correct_cost(self):
        self.usOfficeAction.generate_ests()
        self.assertEquals(USOAEstimateTemplate.objects.all().aggregate(Sum('official_cost')),
                          USOAEstimate.objects.all().aggregate(Sum('official_cost')))

    def test_generate_ests_creates_three_law_firm_ests(self):
        self.usOfficeAction.generate_ests()
        self.assertEquals(LawFirmEst.objects.all().count(), 3)
        self.assertEquals(LawFirmEstTemplate.objects.all().count(),
                          LawFirmEst.objects.all().count())

    def test_generate_ests_creates_correct_cost_law_firm_ests(self):
        self.usOfficeAction.generate_ests()
        self.assertEquals(LawFirmEstTemplate.objects.all().aggregate(Sum('law_firm_cost')),
                          LawFirmEst.objects.all().aggregate(Sum('law_firm_cost')))

    def test_generate_ests_creates_3_of_4_ests(self):
        conditions = LineEstimationTemplateConditionsFactory(condition_entity_size=EntitySizeFactory(micro=True))
        USOAEstimateTemplateFactory.create(country=self.country_us,
                                           appl_type=self.applType_utility,
                                           conditions=conditions)
        self.usOfficeAction.generate_ests()
        self.assertEquals(USOAEstimateTemplate.objects.all().count(), 4)
        self.assertEquals(USOAEstimate.objects.all().count(), 3)

    def test_generate_ests_creates_correct_date(self):
        conditions = LineEstimationTemplateConditionsFactory(condition_entity_size=EntitySizeFactory(small=True))
        USOAEstimateTemplateFactory.create(country=self.country_us,
                                           appl_type=self.applType_utility,
                                           conditions=conditions)
        entitySize = EntitySizeFactory(small=True)
        USUtilityApplicationFactory(country=self.country_us,
                                    details=ApplDetailsFactory(entity_size=entitySize))
        usOfficeAction = USOfficeActionFactory(application=self.application)
        usOfficeAction.generate_ests()
        self.assertEquals(USOAEstimate.objects.all().first().date,
                          USOAEstimateTemplate.objects.all().first().date_diff + usOfficeAction.date_office_action)


class PublicationTest(TestCase):

    def setUp(self):
        self.country_us = CountryFactory(US=True)
        self.applType_prov = ApplTypeFactory(prov=True)
        self.applType_pct = ApplTypeFactory(pct=True)
        self.applType_utility = ApplTypeFactory(utility=True)
        self.entity_size = EntitySizeFactory(us_small=True)
        self.details = ApplDetailsFactory(entity_size=self.entity_size)
        self.application = USUtilityApplicationFactory(country=self.country_us, details=self.details,
                                                       date_filing=datetime.now().date())
        self.usPublication = PublicationFactory(application=self.application)
        self.conditions_one = LineEstimationTemplateConditionsFactory(
            condition_entity_size=EntitySizeFactory(us_small=True))
        self.conditions_two = LineEstimationTemplateConditionsFactory(
            condition_entity_size=EntitySizeFactory(us_small=True))
        self.conditions_three = LineEstimationTemplateConditionsFactory(
            condition_entity_size=EntitySizeFactory(us_small=True))
        self.publEstTemplate_one = PublicationEstTemplateFactory(country=self.country_us,
                                                                 conditions=self.conditions_one,
                                                                 appl_type=self.applType_utility)
        self.publEstTemplate_two = PublicationEstTemplateFactory(country=self.country_us,
                                                                 conditions=self.conditions_two,
                                                                 appl_type=self.applType_utility)
        self.publEstTemplate_three = PublicationEstTemplateFactory(country=self.country_us,
                                                                   conditions=self.conditions_three,
                                                                   appl_type=self.applType_utility)

    # def test_all(self):

    def test_generate_ests_creates_three_ests(self):
        self.usPublication.generate_ests()
        self.assertEquals(PublicationEst.objects.all().count(), 3)
        self.assertEquals(PublicationEstTemplate.objects.all().count(),
                          PublicationEst.objects.all().count())

    def test_generate_ests_creates_correct_cost(self):
        self.usPublication.generate_ests()
        self.assertEquals(PublicationEstTemplate.objects.all().aggregate(Sum('official_cost')),
                          PublicationEst.objects.all().aggregate(Sum('official_cost')))

    def test_generate_ests_creates_three_law_firm_ests(self):
        self.usPublication.generate_ests()
        self.assertEquals(PublicationEst.objects.all().count(), 3)
        self.assertEquals(PublicationEstTemplate.objects.all().count(),
                          PublicationEst.objects.all().count())

    def test_generate_ests_creates_correct_cost_law_firm_ests(self):
        self.usPublication.generate_ests()
        self.assertEquals(LawFirmEstTemplate.objects.all().aggregate(Sum('law_firm_cost')),
                          LawFirmEst.objects.all().aggregate(Sum('law_firm_cost')))

    def test_generate_ests_creates_3_of_4_ests(self):
        conditions = LineEstimationTemplateConditionsFactory(condition_entity_size=EntitySizeFactory(micro=True))
        PublicationEstTemplateFactory.create(country=self.country_us,
                                             appl_type=self.applType_utility,
                                             conditions=conditions)
        self.usPublication.generate_ests()
        self.assertEquals(PublicationEstTemplate.objects.all().count(), 4)
        self.assertEquals(PublicationEst.objects.all().count(), 3)

    def test_generate_ests_creates_correct_date(self):
        self.usPublication.generate_ests()
        self.assertEquals(PublicationEst.objects.all().first().date,
                          self.publEstTemplate_one.date_diff + self.usPublication.date_publication)
