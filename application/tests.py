from dateutil.relativedelta import relativedelta
from django.db.models import Sum
from django.test import TestCase

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
from famform.factories import ApplOptionsFactory, PublOptionFactory, AllowOptionsFactory, OAOptionsFactory, \
    IssueOptionsFactory
from famform.models import OAOptions
from family.factories import FamilyFactory
from transform.factories import DefaultFilingTransformFactory, CustomFilingTransformFactory, IssueTransformFactory, \
    AllowanceTransformFactory, OATransformFactory, PublicationTransformFactory, CountryOANumFactory, \
    DefaultCountryOANumFactory, DefaultPublTransformFactory, DefaultOATransformFactory, \
    DefaultAllowanceTransformFactory, DefaultIssueTransformFactory
from user.factories import UserFactory
from .factories import USUtilityApplicationFactory, USOfficeActionFactory, IssuanceFactory, \
    AllowanceFactory, PublicationFactory, BaseUtilityApplicationFactory, OfficeActionFactory, ApplDetailsFactory
from .models import BaseApplication
from .models.allowance import Allowance
from .models.issue import Issue
from .models.publication import Publication
from .models.usOfficeAction import USOfficeAction
from .models.utilityApplication import UtilityApplication


# Create your tests here.

class UtilityApplicationTest(TestCase):

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
        self.oaTrans = OATransformFactory(country=self.country_US)
        self.publTrans = PublicationTransformFactory(country=self.country_US)
        self.countryOANum = CountryOANumFactory(country=self.country_US)

        self.filing_template_us = FilingEstimateTemplateFactory(country=self.country_US,
                                                                appl_type=self.applType_utility)
        self.publication_template = PublicationEstTemplateFactory(country=self.country_US)
        self.oa_template = OAEstimateTemplateFactory(country=self.country_JP)
        self.oa_template = OAEstimateTemplateFactory(country=self.country_CN)
        self.oa_template = USOAEstimateTemplateFactory()
        self.allowance_template = AllowanceEstTemplateFactory(country=self.country_US)
        self.issue_template = IssueEstTemplateFactory(country=self.country_US)

        self.applOption = ApplOptionsFactory(country=self.country_US, appl_type=self.applType_utility)
        self.publOption = PublOptionFactory(appl=self.applOption)
        self.oaOption = OAOptionsFactory(appl=self.applOption)
        self.allowOption = AllowOptionsFactory(appl=self.applOption)
        self.issueOption = IssueOptionsFactory(appl=self.applOption)

    def test_create_full_creates_Publication(self):
        UtilityApplication.objects.create_full(options=self.applOption,
                                               user=self.user, family_id=self.family.id)

        uAppl = BaseApplication.objects.get(user=self.user)
        date_publication = uAppl.date_filing + self.publOption.date_diff
        self.assertEquals(date_publication, Publication.objects.first().date_publication)

    def test_create_full_creates_oa(self):
        UtilityApplication.objects.create_full(options=self.applOption,
                                               user=self.user, family_id=self.family.id)

        uAppl = BaseApplication.objects.get(user=self.user)
        # relativedelta is calced by combining options in Setup
        date_allowance = uAppl.date_filing + relativedelta(years=1)
        self.assertEquals(date_allowance, USOfficeAction.objects.first().date_office_action)

    def test_create_full_creates_allowance(self):
        UtilityApplication.objects.create_full(options=self.applOption,
                                               user=self.user, family_id=self.family.id)
        uAppl = BaseApplication.objects.get(user=self.user)
        # relativedelta is calced by combining options in Setup
        oa_agg = self.applOption.oaoptions_set.all().aggregate(date_diff=Sum('date_diff'))
        allow_diff = self.applOption.allowoptions.date_diff
        date_allowance = uAppl.date_filing + oa_agg['date_diff'] + allow_diff
        self.assertEquals(date_allowance, Allowance.objects.first().date_allowance)

    def test_create_full_creates_issue(self):
        UtilityApplication.objects.create_full(options=self.applOption,
                                               user=self.user,
                                               family_id=self.family.id)
        uAppl = BaseApplication.objects.get(user=self.user)
        oa_agg = self.applOption.oaoptions_set.all().aggregate(date_diff=Sum('date_diff'))
        allow_diff = self.applOption.allowoptions.date_diff
        issue_diff = self.applOption.issueoptions.date_diff
        date_issuance = uAppl.date_filing + oa_agg['date_diff'] + allow_diff + issue_diff
        self.assertEquals(date_issuance, Issue.objects.first().date_issuance)

    def test_generate_filing_est(self):
        UtilityApplication.objects.create_full(options=self.applOption,
                                               user=self.user,
                                               family_id=self.family.id)
        uAppl = BaseApplication.objects.get(user=self.user)
        self.assertEquals(FilingEstimate.objects.get(application=uAppl).official_cost,
                          FilingEstimateTemplate.objects.first().official_cost)

    def test_create_full_publication_est(self):
        UtilityApplication.objects.create_full(options=self.applOption,
                                               user=self.user, family_id=self.family.id)
        publEstTemp = PublicationEstTemplate.objects.all()
        self.assertEquals(PublicationEstTemplate.objects.first().official_cost,
                          PublicationEst.objects.all().first().official_cost
                          )

    def test_create_full_oa_est(self):
        UtilityApplication.objects.create_full(options=self.applOption,
                                               user=self.user, family_id=self.family.id)
        self.assertEquals(USOAEstimateTemplate.objects.first().official_cost,
                          USOAEstimate.objects.all().first().official_cost
                          )

    def test_create_full_allowance_est(self):
        UtilityApplication.objects.create_full(options=self.applOption,
                                               user=self.user, family_id=self.family.id)
        self.assertEquals(AllowanceEstTemplate.objects.first().official_cost,
                          AllowanceEst.objects.all().first().official_cost
                          )

    def test_create_full_issue_est(self):
        UtilityApplication.objects.create_full(options=self.applOption,
                                               user=self.user, family_id=self.family.id)
        self.assertEquals(IssueEstTemplate.objects.first().official_cost,
                          IssueEst.objects.all().first().official_cost
                          )


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
        self.publication_template = PublicationEstTemplateFactory(country=self.country_US)
        self.oa_template = USOAEstimateTemplateFactory()
        self.oa_template_foa = USOAEstimateTemplateFactory(oa_type='FOA')
        self.allowance_template = AllowanceEstTemplateFactory(country=self.country_US)
        self.issue_template = IssueEstTemplateFactory(country=self.country_US)

        self.applOption = ApplOptionsFactory(country=self.country_US, appl_type=self.applType_utility)
        self.publOption = PublOptionFactory(appl=self.applOption)
        self.oaOption = OAOptionsFactory(appl=self.applOption)
        self.oaOption_two = OAOptionsFactory(appl=self.applOption, oa_prev=self.oaOption)
        self.oaOption_three = OAOptionsFactory(appl=self.applOption, oa_prev=self.oaOption_two)
        self.oaOption_four = OAOptionsFactory(appl=self.applOption, oa_prev=self.oaOption_three)
        self.allowOption = AllowOptionsFactory(appl=self.applOption)
        self.issueOption = IssueOptionsFactory(appl=self.applOption)

    def test_creates_only_one_primary_oas(self):
        application = USUtilityApplicationFactory(country=self.country_US)
        oa_options = OAOptions.objects.filter(appl=self.applOption)
        application._generate_oa(oa_options)
        oas = USOfficeAction.objects.all()
        self.assertTrue(oas.filter(oa_prev=None).count() == 1)

    def test_create_multiple_oas_nfoa_foa_nfoa_foa(self):
        application = USUtilityApplicationFactory(country=self.country_US)
        oa_options=OAOptions.objects.filter(appl=self.applOption)
        application._generate_oa(oa_options)
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
        oa_options = OAOptions.objects.filter(appl=self.applOption)
        application._generate_oa(oa_options)
        oas = USOfficeAction.objects.all()

        oa_first = [x for x in oas if x.oa_prev is None][0]
        oa_option_first = [y for y in oa_options if y.oa_prev is None][0]
        self.assertEquals(oa_first.date_office_action,
                          (oa_option_first.date_diff + application.date_filing).date())
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


class AllowanceTest(TestCase):

    def setUp(self):
        self.country_us = CountryFactory(US=True)
        self.applType = ApplTypeFactory(utility=True)
        self.application = USUtilityApplicationFactory(country=self.country_us)
        self.usAllowance = AllowanceFactory(application=self.application)
        AllowanceEstTemplateFactory.create_batch(3, country=self.country_us,
                                                 appl_type=self.applType)

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
        conditions = LineEstimationTemplateConditionsFactory(condition_entity_size=EntitySizeFactory(small=True))
        AllowanceEstTemplateFactory.create(country=self.country_us,
                                           appl_type=self.applType,
                                           conditions=conditions)
        self.usAllowance.generate_ests()
        self.assertEquals(AllowanceEstTemplate.objects.all().count(), 4)
        self.assertEquals(AllowanceEst.objects.all().count(), 3)

    def test_generate_ests_creates_correct_date(self):
        conditions = LineEstimationTemplateConditionsFactory(condition_entity_size=EntitySizeFactory(small=True))
        allowEstTemp = AllowanceEstTemplateFactory.create(country=self.country_us,
                                       appl_type=self.applType,
                                       conditions=conditions)
        entitySize = EntitySizeFactory(small=True)
        application = USUtilityApplicationFactory(country=self.country_us,
                                                  details=ApplDetailsFactory(entity_size=entitySize))
        usAllow = AllowanceFactory(application=application)
        usAllow.generate_ests()
        self.assertEquals(AllowanceEst.objects.all().first().date,
                          allowEstTemp.date_diff + usAllow.date_allowance)


class IssueTest(TestCase):

    def setUp(self):
        self.country_us = CountryFactory(US=True)
        self.applType = ApplTypeFactory(utility=True)
        self.application = USUtilityApplicationFactory(country=self.country_us)
        self.usIssuance = IssuanceFactory(application=self.application)
        IssueEstTemplateFactory.create_batch(3, country=self.country_us,
                                                 appl_type=self.applType)

    def test_generate_ests_creates_three_ests(self):
        self.usIssuance.generate_ests()
        self.assertEquals(IssueEstTemplate.objects.all().count(), 3)
        self.assertEquals(IssueEstTemplate.objects.all().count(),
                          IssueEst.objects.all().count())

    def test_generate_ests_creates_correct_cost(self):
        self.usIssuance.generate_ests()
        self.assertEquals(IssueEstTemplate.objects.all().aggregate(Sum('official_cost')),
                          IssueEst.objects.all().aggregate(Sum('official_cost')))

    def test_generate_ests_creates_three_law_firm_ests(self):
        self.usIssuance.generate_ests()
        self.assertEquals(IssueEst.objects.all().count(), 3)
        self.assertEquals(IssueEstTemplate.objects.all().count(),
                          IssueEst.objects.all().count())

    def test_generate_ests_creates_correct_cost_law_firm_ests(self):
        self.usIssuance.generate_ests()
        self.assertEquals(LawFirmEstTemplate.objects.all().aggregate(Sum('law_firm_cost')),
                          LawFirmEst.objects.all().aggregate(Sum('law_firm_cost')))

    def test_generate_ests_creates_3_of_4_ests(self):
        conditions = LineEstimationTemplateConditionsFactory(condition_entity_size=EntitySizeFactory(small=True))
        IssueEstTemplateFactory.create(country=self.country_us,
                                           appl_type=self.applType,
                                           conditions=conditions)
        self.usIssuance.generate_ests()
        self.assertEquals(IssueEstTemplate.objects.all().count(), 4)
        self.assertEquals(IssueEst.objects.all().count(), 3)

    def test_generate_ests_creates_correct_date(self):
        conditions = LineEstimationTemplateConditionsFactory(condition_entity_size=EntitySizeFactory(small=True))
        issueEstTemp = IssueEstTemplateFactory.create(country=self.country_us,
                                             appl_type=self.applType,
                                             conditions=conditions)
        entitySize = EntitySizeFactory(small=True)
        application = USUtilityApplicationFactory(country=self.country_us,
                                                  details=ApplDetailsFactory(entity_size=entitySize))
        usIssue = IssuanceFactory(application=application)
        usIssue.generate_ests()
        self.assertEquals(IssueEst.objects.all().first().date,
                          issueEstTemp.date_diff + usIssue.date_issuance)

class OfficeActionTest(TestCase):

    def setUp(self):
        self.country_cn = CountryFactory(CN=True)
        self.applType = ApplTypeFactory(utility=True)
        self.application = BaseUtilityApplicationFactory(country=self.country_cn)
        self.cnOfficeAction = OfficeActionFactory(application=self.application)
        OAEstimateTemplateFactory.create_batch(3, country=self.country_cn,
                                                 appl_type=self.applType)

    def test_generate_ests_creates_three_ests(self):
        self.cnOfficeAction.generate_ests()
        self.assertEquals(OAEstimateTemplate.objects.all().count(), 3)
        self.assertEquals(OAEstimateTemplate.objects.all().count(),
                          OAEstimate.objects.all().count())

    def test_generate_ests_creates_correct_cost(self):
        self.cnOfficeAction.generate_ests()
        self.assertEquals(OAEstimateTemplate.objects.all().aggregate(Sum('official_cost')),
                          OAEstimate.objects.all().aggregate(Sum('official_cost')))

    def test_generate_ests_creates_three_law_firm_ests(self):
        self.cnOfficeAction.generate_ests()
        self.assertEquals(LawFirmEst.objects.all().count(), 3)
        self.assertEquals(LawFirmEstTemplate.objects.all().count(),
                          LawFirmEst.objects.all().count())

    def test_generate_ests_creates_correct_cost_law_firm_ests(self):
        self.cnOfficeAction.generate_ests()
        self.assertEquals(LawFirmEstTemplate.objects.all().aggregate(Sum('law_firm_cost')),
                          LawFirmEst.objects.all().aggregate(Sum('law_firm_cost')))

    def test_generate_ests_creates_3_of_4_ests(self):
        conditions = LineEstimationTemplateConditionsFactory(condition_entity_size=EntitySizeFactory(small=True))
        OAEstimateTemplateFactory.create(country=self.country_cn,
                                           appl_type=self.applType,
                                           conditions=conditions)
        self.cnOfficeAction.generate_ests()
        self.assertEquals(OAEstimateTemplate.objects.all().count(), 4)
        self.assertEquals(OAEstimate.objects.all().count(), 3)

    def test_generate_ests_creates_correct_date(self):
        conditions = LineEstimationTemplateConditionsFactory(condition_entity_size=EntitySizeFactory(small=True))
        OAEstimateTemplateFactory.create(country=self.country_cn,
                                         appl_type=self.applType,
                                         conditions=conditions)
        entitySize = EntitySizeFactory(small=True)
        BaseUtilityApplicationFactory(country=self.country_cn,
                                                    details=ApplDetailsFactory(entity_size=entitySize))
        cnOfficeAction = OfficeActionFactory(application=self.application)
        cnOfficeAction.generate_ests()
        self.assertEquals(OAEstimate.objects.all().first().date,
                         OAEstimateTemplate.objects.all().first().date_diff + cnOfficeAction.date_office_action)


class USOfficeActionTest(TestCase):

    def setUp(self):
        self.country_us = CountryFactory(US=True)
        self.applType = ApplTypeFactory(utility=True)
        self.application = USUtilityApplicationFactory(country=self.country_us)
        self.usOfficeAction = USOfficeActionFactory(application=self.application)
        USOAEstimateTemplateFactory.create_batch(3, country=self.country_us,
                                                 appl_type=self.applType)

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
        conditions = LineEstimationTemplateConditionsFactory(condition_entity_size=EntitySizeFactory(small=True))
        USOAEstimateTemplateFactory.create(country=self.country_us,
                                           appl_type=self.applType,
                                           conditions=conditions)
        self.usOfficeAction.generate_ests()
        self.assertEquals(USOAEstimateTemplate.objects.all().count(), 4)
        self.assertEquals(USOAEstimate.objects.all().count(), 3)

    def test_generate_ests_creates_correct_date(self):
        conditions = LineEstimationTemplateConditionsFactory(condition_entity_size=EntitySizeFactory(small=True))
        USOAEstimateTemplateFactory.create(country=self.country_us,
                                         appl_type=self.applType,
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
        self.applType = ApplTypeFactory(utility=True)
        self.application = USUtilityApplicationFactory(country=self.country_us)
        self.usPublication = PublicationFactory(application=self.application)
        PublicationEstTemplateFactory.create_batch(3, country=self.country_us,
                                                 appl_type=self.applType)

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
        conditions = LineEstimationTemplateConditionsFactory(condition_entity_size=EntitySizeFactory(small=True))
        PublicationEstTemplateFactory.create(country=self.country_us,
                                           appl_type=self.applType,
                                           conditions=conditions)
        self.usPublication.generate_ests()
        self.assertEquals(PublicationEstTemplate.objects.all().count(), 4)
        self.assertEquals(PublicationEst.objects.all().count(), 3)

    def test_generate_ests_creates_correct_date(self):
        conditions = LineEstimationTemplateConditionsFactory(condition_entity_size=EntitySizeFactory(small=True))
        publEstTemp = PublicationEstTemplateFactory.create(country=self.country_us,
                                             appl_type=self.applType,
                                             conditions=conditions)
        entitySize = EntitySizeFactory(small=True)
        application = USUtilityApplicationFactory(country=self.country_us,
                                    details=ApplDetailsFactory(entity_size=entitySize))
        usPublication = PublicationFactory(application=application)
        usPublication.generate_ests()
        self.assertEquals(PublicationEst.objects.all().first().date,
                          publEstTemp.date_diff + usPublication.date_publication)