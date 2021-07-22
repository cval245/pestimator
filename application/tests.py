from django.test import TestCase
from characteristics.factories import ApplTypeFactory, CountryFactory, EntitySizeFactory
from estimation.factories import FilingEstimateTemplateFactory, PublicationEstTemplateFactory, \
    OAEstimateTemplateFactory, AllowanceEstTemplateFactory, IssueEstTemplateFactory, USOAEstimateTemplateFactory
from famform.factories import ApplOptionsFactory, PublOptionFactory, AllowOptionsFactory, OAOptionsFactory, \
    IssueOptionsFactory
from family.factories import FamilyFactory
from transform.factories import DefaultFilingTransformFactory, CustomFilingTransformFactory, IssueTransformFactory, \
    AllowanceTransformFactory, OATransformFactory, PublicationTransformFactory, CountryOANumFactory, \
    DefaultCountryOANumFactory, DefaultPublTransformFactory, DefaultOATransformFactory, \
    DefaultAllowanceTransformFactory, DefaultIssueTransformFactory
from user.factories import UserFactory
from .models import BaseApplication
from .models.issue import Issue
from .models.allowance import Allowance
from .models.publication import Publication
from .models.usOfficeAction import USOfficeAction
from .models.utilityApplication import UtilityApplication
from dateutil.relativedelta import relativedelta
from django.db.models import Sum
from estimation.models import \
    OAEstimate, OAEstimateTemplate, \
    PublicationEstTemplate, \
    PublicationEst, AllowanceEst, IssueEst, USOAEstimateTemplate, \
    USOAEstimate, FilingEstimate

# Create your tests here.

class UtilityApplicationTest(TestCase):

    def setUp(self):
        self.user = UserFactory()
        self.applType_prov = ApplTypeFactory(prov=True)
        self.applType_pct = ApplTypeFactory(pct=True)
        self.applType_utility = ApplTypeFactory(utility=True)
        self.country_US = CountryFactory(US=True)
        self.country_CN = CountryFactory(CN=True)
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
                          self.filing_template_us.official_cost)

    def test_create_full_publication_est(self):

        UtilityApplication.objects.create_full(options=self.applOption,
                                               user=self.user, family_id=self.family.id)
        publEstTemp = PublicationEstTemplate.objects.all()
        self.assertEquals(self.publication_template.official_cost,
                          PublicationEst.objects.all().first().official_cost
                          )

    def test_create_full_oa_est(self):
        UtilityApplication.objects.create_full(options=self.applOption,
                                               user=self.user, family_id=self.family.id)
        a = OAEstimateTemplate.objects.all()
        b = OAEstimate.objects.all()
        c = vars(USOAEstimateTemplate.objects.all().first())
        d = vars(USOAEstimateTemplate.objects.all().first().conditions)
        self.assertEquals(self.oa_template.official_cost,
                          USOAEstimate.objects.all().first().official_cost
                          )

    def test_create_full_allowance_est(self):
        UtilityApplication.objects.create_full(options=self.applOption,
                                               user=self.user, family_id=self.family.id)
        self.assertEquals(self.allowance_template.official_cost,
                          AllowanceEst.objects.all().first().official_cost
                          )

    def test_create_full_issue_est(self):
        UtilityApplication.objects.create_full(options=self.applOption,
                                               user=self.user, family_id=self.family.id)
        self.assertEquals(self.issue_template.official_cost,
                          IssueEst.objects.all().first().official_cost

                          )
