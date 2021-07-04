from django.test import TestCase
from datetime import date
from djmoney.money import Money
from django.contrib.auth import get_user_model
from transform.models import DefaultFilingTransform, CustomFilingTransform,\
    IssueTransform, AllowanceTransform, OATransform, PublicationTransform,\
    CountryOANum, DefaultCountryOANum, DefaultPublTransform,\
    DefaultOATransform, DefaultAllowanceTransform, DefaultIssueTransform
from characteristics.models import ApplType, Country, EntitySize
from dateutil.relativedelta import relativedelta
from .models import FamOptions, ApplOptions, PublOptions, OAOptions,\
    FamEstFormData, AllowOptions, IssueOptions
from estimation.models import LineEstimationTemplateConditions, FilingEstimateTemplate,\
    OAEstimate, OAEstimateTemplate,\
    PublicationEstTemplate, AllowanceEstTemplate, IssueEstTemplate,\
    PublicationEst, AllowanceEst, IssueEst

from family.models import Family
from application.models import ApplDetails, BaseApplication, ProvApplication

# Create your tests here.

class FamFormApplicationTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(username='test',
                                                         password='Belgrade2010',
                                                         email='c.val@tutanota.com')
        self.applType = ApplType.objects.create(application_type='prov')
        self.applType_pct = ApplType.objects.create(application_type='pct')
        self.applType_utility = ApplType.objects.create(application_type='utility')
        self.country = Country.objects.create(country='US', currency_name='USD')
        self.country_CN = Country.objects.create(country='CN', currency_name='CNY')
        self.countries = [self.country]
        self.family = Family.objects.create(user=self.user, family_name='family_name',
                                            family_no='family_no')
        self.entitySize = EntitySize.objects.create(entity_size='test')

        self.applDetails = ApplDetails.objects.create(
            num_indep_claims=1,
            num_pages=1,
            num_claims=1,
            num_drawings=1,
            entity_size=self.entitySize)

        self.filing_date = date(2020, 1, 1)

        self.dfltFilTrans = DefaultFilingTransform.objects.create(appl_type=self.applType,
                                                                  date_diff=relativedelta(years=2))
        self.dfltFilTrans_pct = DefaultFilingTransform.objects.create(appl_type=self.applType_pct,
                                                                  date_diff=relativedelta(years=2))
        self.dfltFilTrans_pct = DefaultFilingTransform.objects.create(
            appl_type=self.applType_utility,
            date_diff=relativedelta(years=2))

        self.customFilTrans = CustomFilingTransform.objects.create(appl_type=self.applType,
                                                                   prev_appl_type=None,
                                                                   country=self.country,
                                                                   date_diff=relativedelta(years=3))
        self.issTrans = IssueTransform.objects.create(country=self.country,
                                                      date_diff=relativedelta(years=4))
        self.allowTran = AllowanceTransform.objects.create(country=self.country,
                                                           date_diff=relativedelta(years=5))
        self.OATrans = OATransform.objects.create(country=self.country,
                                                  date_diff=relativedelta(years=6))
        self.publTrans = PublicationTransform.objects.create(country=self.country,
                                                             date_diff=relativedelta(years=7))
        self.countryOANum = CountryOANum.objects.create(country=self.country, oa_total=3)
        self.defaultCountryOANum = DefaultCountryOANum.objects.create(oa_total=2)

        self.famOpt = FamOptions.objects.create(family=self.family)

        self.famFormData = FamEstFormData.objects.create(
            user=self.user,
            family=self.family,
            init_appl_filing_date=date(2020, 1, 1),
            init_appl_country=self.country,
            init_appl_type=self.applType,
            init_appl_indep_claims=1,
            init_appl_claims=10,
            init_appl_drawings=3,
            init_appl_pages=12,
            method=True,
            meth_country=self.country,
            entity_size=self.entitySize,
        )
        self.famFormData.countries.set(self.countries)
        self.conditions = LineEstimationTemplateConditions.objects.create(
            condition_claims_min=0,
            #condition_claims_max=Null,
            condition_drawings_min=0,
            #condition_drawings_max=0,
            condition_pages_min=0,
            #condition_pages_max=0,
            condition_entity_size=self.entitySize,
        )
        self.filing_template = FilingEstimateTemplate.objects.create(
            date_diff=relativedelta(years=1),
            official_cost=Money(1, 'USD'),
            country=self.country,
            conditions=self.conditions,
        )
        self.publication_template = PublicationEstTemplate.objects.create(
            date_diff=relativedelta(years=1),
            official_cost=Money(2, 'USD'),
            country=self.country,
            conditions=self.conditions,
        )
        self.oa_template = OAEstimateTemplate.objects.create(
            date_diff=relativedelta(years=1),
            official_cost=Money(3, 'USD'),
            country=self.country,
            conditions=self.conditions,
        )
        self.allowance_template = AllowanceEstTemplate.objects.create(
            date_diff=relativedelta(years=1),
            official_cost=Money(4, 'USD'),
            country=self.country,
            conditions=self.conditions,
        )
        self.issue_template = IssueEstTemplate.objects.create(
            date_diff=relativedelta(years=1),
            official_cost=Money(5, 'USD'),
            country=self.country,
            conditions=self.conditions,
        )

    def test_generate_family_options_creates_first_appl(self):
        self.famFormData.generate_family_options()
        applOptCount = ApplOptions.objects.all().count()
        self.assertEquals(3, applOptCount)

    def test_generate_family_options_creates_publ_est(self):
        self.famFormData.generate_family_options()
        self.assertEquals(self.publication_template.official_cost,
                          PublicationEst.objects.all().first().official_cost)

   


class FamOptionsTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(username='test',
                                                         password='Belgrade2010',
                                                         email='c.val@tutanota.com')
        self.applType = ApplType.objects.create(application_type='default')
        self.country = Country.objects.create(country='US', currency_name='USD')
        self.country_CN = Country.objects.create(country='CN', currency_name='CNY')
        self.countries = [self.country]
        self.family = Family.objects.create(user=self.user, family_name='family_name',
                                            family_no='family_no')
        self.entitySize = EntitySize.objects.create(entity_size='test')

        self.applDetails = ApplDetails.objects.create(
            num_indep_claims=1,
            num_pages=1,
            num_claims=1,
            num_drawings=1,
            entity_size=self.entitySize)

        self.filing_date = date(2020, 1, 1)

        self.dfltFilTrans = DefaultFilingTransform.objects.create(appl_type=self.applType,
                                                                  date_diff=relativedelta(years=2))
        self.customFilTrans = CustomFilingTransform.objects.create(appl_type=self.applType,
                                                                   prev_appl_type=None,
                                                                   country=self.country,
                                                                   date_diff=relativedelta(years=3))
        self.issTrans = IssueTransform.objects.create(country=self.country,
                                                      date_diff=relativedelta(years=4))
        self.allowTran = AllowanceTransform.objects.create(country=self.country,
                                                           date_diff=relativedelta(years=5))
        self.OATrans = OATransform.objects.create(country=self.country,
                                                  date_diff=relativedelta(years=6))
        self.publTrans = PublicationTransform.objects.create(country=self.country,
                                                             date_diff=relativedelta(years=7))
        self.countryOANum = CountryOANum.objects.create(country=self.country, oa_total=3)
        self.defaultCountryOANum = DefaultCountryOANum.objects.create(oa_total=2)

        self.famOpt = FamOptions.objects.create(family=self.family)

        self.dfltpublTransform = DefaultPublTransform.objects.create(
            appl_type=self.applType,
            date_diff=relativedelta(months=6))

        self.dfltOATransform = DefaultOATransform.objects.create(
            appl_type=self.applType,
            date_diff=relativedelta(months=6))

        self.dfltAllowTransform = DefaultAllowanceTransform.objects.create(
            appl_type=self.applType,
            date_diff=relativedelta(months=6))

        self.dfltIssueTransform = DefaultIssueTransform.objects.create(
            appl_type=self.applType,
            date_diff=relativedelta(months=6))


    def test_calc_filing_date_DefaultFilingTransform(self):
        beg_date = date(2020, 1, 1)
        date_filing = self.famOpt._calc_filing_date(
            country=self.country_CN,
            appl_type=self.applType,
            prev_appl_type=None,
            prev_date=beg_date,
            first_appl_bool=False)
        dflt_date_filing = self.dfltFilTrans.date_diff + beg_date
        self.assertEquals(date_filing, dflt_date_filing)

    def test_calc_filing_date_CustomFilingTransform(self):
        beg_date = date(2020, 1, 1)
        date_filing = self.famOpt._calc_filing_date(
            country=self.country,
            appl_type=self.applType,
            prev_appl_type=None,
            prev_date=beg_date,
            first_appl_bool=False)
        cstm_date_filing = self.customFilTrans.date_diff + beg_date
        self.assertEquals(date_filing, cstm_date_filing)

    def test_calc_oa_num_returns_CountryOANum(self):
        oa_total = self.famOpt._calc_oa_num(self.country)
        self.assertEquals(oa_total, self.countryOANum.oa_total)

    def test_calc_oa_num_returns_DefaultCountryOANum(self):
        oa_total = self.famOpt._calc_oa_num(self.country_CN)
        self.assertEquals(oa_total, self.defaultCountryOANum.oa_total)

    def test_generate_appl_creates_applOption(self):
        applOption = self.famOpt.generate_appl(
            details=self.applDetails,
            country=self.country_CN,
            appl_type=self.applType,
            prev_appl_type=None,
            prev_date=date(2020, 1, 1),
            first_appl_bool=False)

        self.assertEquals(applOption, ApplOptions.objects.first())


    def test_generate_appl_option_returns_created_applOption(self):
        oa_total = 2
        ret = self.famOpt.generate_appl_option(self.country, self.applDetails, self.applType,
                                               self.filing_date, oa_total)
        self.assertEquals(ret, ApplOptions.objects.all().first())

    def test_generate_appl_option_creates_publOption(self):
        oa_total = 2
        ret=self.famOpt.generate_appl_option(self.country, self.applDetails, self.applType,
                                               self.filing_date, oa_total)
        self.assertEquals(self.publTrans.date_diff, PublOptions.objects.all().first().date_diff)


    def test_generate_appl_option_creates_AllowOption(self):
        oa_total = 2
        ret=self.famOpt.generate_appl_option(self.country, self.applDetails, self.applType,
                                               self.filing_date, oa_total)
        self.assertEquals(self.allowTran.date_diff,
                          AllowOptions.objects.all().first().date_diff)

    def test_generate_appl_option_creates_IssueOption(self):
        oa_total = 2
        ret=self.famOpt.generate_appl_option(self.country, self.applDetails, self.applType,
                                               self.filing_date, oa_total)
        self.assertEquals(self.issTrans.date_diff,
                          IssueOptions.objects.all().first().date_diff)

    def test_generate_appl_option_creates_OAOption(self):
        oa_total = 2
        ret=self.famOpt.generate_appl_option(self.country, self.applDetails, self.applType,
                                             self.filing_date, oa_total)
        self.assertEquals(self.OATrans.date_diff,
                          OAOptions.objects.all().first().date_diff)

    def test_generate_appl_option_creates_OAOption_array(self):
        oa_total = 2
        ret=self.famOpt.generate_appl_option(self.country, self.applDetails, self.applType,
                                             self.filing_date, oa_total)
        self.assertEquals(oa_total,
                          OAOptions.objects.all().count())


class ApplOptionsTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='test',
                                                         password='Belgrade2010',
                                                         email='c.val@tutanota.com')
        self.applType = ApplType.objects.create(application_type='default')
        self.country = Country.objects.create(country='US', currency_name='USD')
        self.country_CN = Country.objects.create(country='CN', currency_name='CNY')
        self.countries = [self.country]
        self.family = Family.objects.create(user=self.user, family_name='family_name',
                                            family_no='family_no')
        self.entitySize = EntitySize.objects.create(entity_size='test')

        self.applDetails = ApplDetails.objects.create(
            num_indep_claims=1,
            num_pages=1,
            num_claims=1,
            num_drawings=1,
            entity_size=self.entitySize)

        self.filing_date = date(2020, 1, 1)

        self.dfltFilTrans = DefaultFilingTransform.objects.create(appl_type=self.applType,
                                                                  date_diff=relativedelta(years=2))
        self.customFilTrans = CustomFilingTransform.objects.create(appl_type=self.applType,
                                                                   prev_appl_type=None,
                                                                   country=self.country,
                                                                   date_diff=relativedelta(years=3))
        self.issTrans = IssueTransform.objects.create(country=self.country,
                                                      date_diff=relativedelta(years=4))
        self.allowTrans = AllowanceTransform.objects.create(country=self.country,
                                                           date_diff=relativedelta(years=5))
        self.OATrans = OATransform.objects.create(country=self.country,
                                                  date_diff=relativedelta(years=6))
        self.publTrans = PublicationTransform.objects.create(country=self.country,
                                                             date_diff=relativedelta(years=7))
        self.countryOANum = CountryOANum.objects.create(country=self.country, oa_total=3)
        self.defaultCountryOANum = DefaultCountryOANum.objects.create(oa_total=2)

        self.famOpt = FamOptions.objects.create(family=self.family)

        self.dfltpublTransform = DefaultPublTransform.objects.create(
            appl_type=self.applType,
            date_diff=relativedelta(months=1))

        self.dfltOATransform = DefaultOATransform.objects.create(
            appl_type=self.applType,
            date_diff=relativedelta(months=2))

        self.dfltAllowTransform = DefaultAllowanceTransform.objects.create(
            appl_type=self.applType,
            date_diff=relativedelta(months=3))

        self.dfltIssueTransform = DefaultIssueTransform.objects.create(
            appl_type=self.applType,
            date_diff=relativedelta(months=4))

        self.applOption = ApplOptions.objects.create(
            appl_type=self.applType,
            details=self.applDetails,
            date_filing=date(2020, 1, 1),
            title='title',
            fam_options=self.famOpt,
            country=self.country,
            prev_appl_options=None
        )
        self.applOption_CN = ApplOptions.objects.create(
            appl_type=self.applType,
            details=self.applDetails,
            date_filing=date(2020, 1, 1),
            title='title',
            fam_options=self.famOpt,
            country=self.country_CN,
            prev_appl_options=None
        )


    def test_create_publ_option_creates_publOption(self):
        publOption = self.applOption.create_publ_option()
        self.assertEquals(publOption, PublOptions.objects.first())

    def test_create_publ_option_returns_default(self):
        publOption = self.applOption_CN.create_publ_option()
        self.assertEquals(publOption.date_diff, self.dfltpublTransform.date_diff)

    def test_create_publ_option_returns_publicationOption(self):
        publOption = self.applOption.create_publ_option()
        self.assertEquals(publOption.date_diff, self.publTrans.date_diff)


    def test_create_allow_option_creates_allowOption(self):
        allowOption = self.applOption.create_allow_option()
        self.assertEquals(allowOption, AllowOptions.objects.first())

    def test_create_allow_option_returns_default(self):
        allowOption = self.applOption_CN.create_allow_option()
        self.assertEquals(allowOption.date_diff, self.dfltAllowTransform.date_diff)

    def test_create_allow_option_returns_allowOption(self):
        allowOption = self.applOption.create_allow_option()
        self.assertEquals(allowOption.date_diff, self.allowTrans.date_diff)


    def test_create_issue_option_creates_issueOption(self):
        issueOption = self.applOption.create_issue_option()
        self.assertEquals(issueOption, IssueOptions.objects.first())

    def test_create_issue_option_returns_default(self):
        issueOption = self.applOption_CN.create_issue_option()
        self.assertEquals(issueOption.date_diff, self.dfltIssueTransform.date_diff)

    def test_create_issue_option_returns_issueOption(self):
        issueOption = self.applOption.create_issue_option()
        self.assertEquals(issueOption.date_diff, self.issTrans.date_diff)


    def test_create_oa_option_creates_oaOption(self):
        oaOption = self.applOption.create_oa_option(oa_prev=None)
        self.assertEquals(oaOption, OAOptions.objects.first())

    def test_create_oa_option_returns_default(self):
        oaOption = self.applOption_CN.create_oa_option(oa_prev=None)
        self.assertEquals(oaOption.date_diff, self.dfltOATransform.date_diff)

    def test_create_oa_option_returns_oaOption(self):
        oaOption = self.applOption.create_oa_option(oa_prev=None)
        self.assertEquals(oaOption.date_diff, self.OATrans.date_diff)

    def test_create_oa_options_correct_length_3(self):
        oa_tot=3
        allOAOptions = self.applOption.create_all_oa_options(oa_tot=oa_tot)
        self.assertEquals(len(allOAOptions), OAOptions.objects.all().count())

    def test_create_oa_options_correct_length_1(self):
        oa_tot=1
        allOAOptions = self.applOption.create_all_oa_options(oa_tot=oa_tot)
        self.assertEquals(len(allOAOptions), OAOptions.objects.all().count())

