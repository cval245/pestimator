from datetime import date, datetime

from dateutil.relativedelta import relativedelta
from django.contrib.auth import get_user_model
from django.test import TestCase

from account.factories import UserProfileFactory
from application.factories import ApplDetailsFactory
from application.models import ApplDetails, BaseApplication, Publication
from characteristics.factories import ApplTypeFactory, CountryFactory, EntitySizeFactory, LanguagesFactory
from characteristics.models import ApplType, Country, EntitySize
from estimation.factories import FilingEstimateTemplateFactory, PublicationEstTemplateFactory, \
    OAEstimateTemplateFactory, AllowanceEstTemplateFactory, IssueEstTemplateFactory, \
    DefaultTranslationEstTemplateFactory
from estimation.models import PublicationEstTemplate, PublicationEst
from family.factories import FamilyFactory
from family.models import Family
from transform.factories import DefaultFilingTransformFactory, CustomFilingTransformFactory, IssueTransformFactory, \
    AllowanceTransformFactory, OATransformFactory, PublicationTransformFactory, CountryOANumFactory, \
    DefaultCountryOANumFactory, DefaultPublTransformFactory, DefaultOATransformFactory, \
    DefaultAllowanceTransformFactory, DefaultIssueTransformFactory
from transform.models import DefaultFilingTransform, CustomFilingTransform, \
    IssueTransform, AllowanceTransform, OATransform, PublicationTransform, \
    CountryOANum, DefaultCountryOANum, DefaultPublTransform, \
    DefaultOATransform, DefaultAllowanceTransform, DefaultIssueTransform
from user.factories import UserFactory
from .factories import FamEstFormDataFactory, ApplOptionsFactory, PublOptionFactory, FamOptionsFactory
from .models import FamOptions, ApplOptions, PublOptions, OAOptions, \
    AllowOptions, IssueOptions


# Create your tests here.

class FamFormApplicationTest(TestCase):

    def setUp(self):
        self.user = UserFactory()
        self.userProfile = UserProfileFactory(user=self.user)
        self.applType_prov = ApplTypeFactory(prov=True)
        self.applType_pct = ApplTypeFactory(pct=True)
        self.applType_utility = ApplTypeFactory(utility=True)
        self.applType_ep = ApplTypeFactory(ep=True)
        self.applType_epvalidation = ApplTypeFactory(epvalidation=True)
        self.applType_nationalphase = ApplTypeFactory(nationalphase=True)
        self.language_english = LanguagesFactory(english=True)
        self.language_chinese = LanguagesFactory(chinese=True)
        self.country_US = CountryFactory(US=True, languages=[self.language_english])
        self.country_CN = CountryFactory(CN=True, languages=[self.language_chinese])
        self.countries = [self.country_US, self.country_CN]
        self.dfltTranslation = DefaultTranslationEstTemplateFactory()
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


        self.famFormData = FamEstFormDataFactory(init_appl_country=self.country_US,
                                                 init_appl_type=self.applType_prov,
                                                 meth_country=self.country_US,
                                                 countries=self.countries)

        self.filing_template_us = FilingEstimateTemplateFactory(country=self.country_US,
                                                                appl_type=self.applType_utility)
        self.publication_template = PublicationEstTemplateFactory(country=self.country_US)
        self.oa_template = OAEstimateTemplateFactory(country=self.country_US)
        self.allowance_template = AllowanceEstTemplateFactory(country=self.country_US)
        self.issue_template = IssueEstTemplateFactory(country=self.country_US)

    def test_generate_family_options_creates_first_appl(self):
        famFormData = FamEstFormDataFactory(
            user=self.user,
            family=self.family,
            init_appl_country=self.country_US,
            init_appl_type=self.applType_prov,
            entity_size=self.entitySize,
            meth_country=self.country_US)
        famFormData.generate_family_options()
        applOptCount = ApplOptions.objects.all().count()
        applCount = BaseApplication.objects.all().count()
        self.assertEquals(applCount, applOptCount)

    def test_generate_family_options_creates_publ_est(self):
        famFormData = FamEstFormDataFactory(init_appl_country=self.country_US,
                                            family=self.family,
                                            init_appl_type=self.applType_prov,
                                            entity_size=self.entitySize,
                                            meth_country=self.country_US,
                                            user=self.user,
                                            countries=self.countries)
        famFormData.generate_family_options()

        self.assertEquals(BaseApplication.objects.all().count() - 1,
                          Publication.objects.all().count())

        self.assertEquals(PublicationEstTemplate.objects.all().count(),
                          PublicationEst.objects.all().count())



class FamOptionsTest(TestCase):

    def setUp(self):
        self.user = UserFactory()
        self.userProfile = UserProfileFactory(user=self.user)
        self.applType_prov = ApplTypeFactory(prov=True)
        self.applType_pct = ApplTypeFactory(pct=True)
        self.applType_utility = ApplTypeFactory(utility=True)
        self.applType_ep = ApplTypeFactory(ep=True)
        self.applType_epvalidation = ApplTypeFactory(epvalidation=True)
        self.applType_nationalphase = ApplTypeFactory(nationalphase=True)
        self.language_english = LanguagesFactory(english=True)
        self.language_chinese = LanguagesFactory(chinese=True)
        self.country_US = CountryFactory(US=True, languages=[self.language_english])
        self.country_CN = CountryFactory(CN=True, languages=[self.language_chinese])
        self.countries = [self.country_US, self.country_CN]
        self.applDetails = ApplDetailsFactory(language=self.language_english)
        self.filing_date = datetime.now()

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

        self.famFormData = FamEstFormDataFactory(init_appl_country=self.country_US,
                                                 init_appl_type=self.applType_prov,
                                                 meth_country=self.country_US,
                                                 countries=self.countries)

        self.filing_template_us = FilingEstimateTemplateFactory(country=self.country_US,
                                                                appl_type=self.applType_utility)
        self.publication_template = PublicationEstTemplateFactory(country=self.country_US)
        self.oa_template = OAEstimateTemplateFactory(country=self.country_US)
        self.allowance_template = AllowanceEstTemplateFactory(country=self.country_US)
        self.issue_template = IssueEstTemplateFactory(country=self.country_US)
        self.famOpt = FamOptionsFactory()


    def test_calc_filing_date_DefaultFilingTransform(self):
        beg_date = date(2020, 1, 1)
        date_filing = self.famOpt._calc_filing_date(
            country=self.country_CN,
            appl_type=self.applType_utility,
            prev_appl_type=None,
            prev_date=beg_date,
            first_appl_bool=False)
        dflt_date_filing = self.dfltFilTrans_utility.date_diff + beg_date
        self.assertEquals(date_filing, dflt_date_filing)

    def test_calc_filing_date_CustomFilingTransform(self):
        beg_date = date(2020, 1, 1)
        date_filing = self.famOpt._calc_filing_date(
            country=self.country_US,
            appl_type=self.applType_utility,
            prev_appl_type=None,
            prev_date=beg_date,
            first_appl_bool=False)
        cstm_date_filing = self.customFilTrans.date_diff + beg_date
        self.assertEquals(date_filing, cstm_date_filing)

    def test_calc_oa_num_returns_CountryOANum(self):
        oa_total = self.famOpt._calc_oa_num(self.country_US)
        self.assertEquals(oa_total, self.countryOANum.oa_total)

    def test_calc_oa_num_returns_DefaultCountryOANum(self):
        oa_total = self.famOpt._calc_oa_num(self.country_CN)
        self.assertEquals(oa_total, self.defaultCountryOANum.oa_total)

    def test_generate_appl_creates_applOption(self):
        applOption = self.famOpt.generate_appl(
            details=self.applDetails,
            country=self.country_CN,
            appl_type=self.applType_utility,
            prev_appl_type=None,
            prev_date=date(2020, 1, 1),
            prev_appl_option=None,
            first_appl_bool=True)

        self.assertEquals(applOption, ApplOptions.objects.first())


    def test_generate_appl_option_returns_created_applOption(self):
        oa_total = 2
        ret = self.famOpt.generate_appl_option(country=self.country_US,
                                               details=self.applDetails,
                                               appl_type=self.applType_utility,
                                               date_filing=self.filing_date,
                                               translation_full_required=False,
                                               oa_total=oa_total,
                                               prev_appl_option=None)

        self.assertEquals(ret, ApplOptions.objects.all().first())

    def test_generate_appl_option_creates_publOption(self):
        oa_total = 2
        ret = self.famOpt.generate_appl_option(country=self.country_US,
                                               details=self.applDetails,
                                               appl_type=self.applType_utility,
                                               date_filing=self.filing_date,
                                               translation_full_required=False,
                                               oa_total=oa_total,
                                               prev_appl_option=None)
        self.assertEquals(self.publTrans.date_diff, PublOptions.objects.all().first().date_diff)


    def test_generate_appl_option_creates_AllowOption(self):
        oa_total = 2
        ret = self.famOpt.generate_appl_option(country=self.country_US,
                                               details=self.applDetails,
                                               appl_type=self.applType_utility,
                                               date_filing=self.filing_date,
                                               translation_full_required=False,
                                               oa_total=oa_total,
                                               prev_appl_option=None)
        self.assertEquals(self.allowTrans.date_diff,
                          AllowOptions.objects.all().first().date_diff)

    def test_generate_appl_option_creates_IssueOption(self):
        oa_total = 2
        ret = self.famOpt.generate_appl_option(country=self.country_US,
                                               details=self.applDetails,
                                               appl_type=self.applType_utility,
                                               date_filing=self.filing_date,
                                               translation_full_required=False,
                                               oa_total=oa_total,
                                               prev_appl_option=None)

        self.assertEquals(self.issTrans.date_diff,
                          IssueOptions.objects.all().first().date_diff)

    def test_generate_appl_option_creates_OAOption(self):
        oa_total = 2
        ret = self.famOpt.generate_appl_option(country=self.country_US,
                                               details=self.applDetails,
                                               appl_type=self.applType_utility,
                                               date_filing=self.filing_date,
                                               translation_full_required=False,
                                               oa_total=oa_total,
                                               prev_appl_option=None)
        self.assertEquals(self.oaTrans.date_diff,
                          OAOptions.objects.all().first().date_diff)

    def test_generate_appl_option_creates_OAOption_array(self):
        oa_total = 2
        ret = self.famOpt.generate_appl_option(country=self.country_US,
                                               details=self.applDetails,
                                               appl_type=self.applType_utility,
                                               date_filing=self.filing_date,
                                               translation_full_required=False,
                                               oa_total=oa_total,
                                               prev_appl_option=None)
        self.assertEquals(oa_total,
                          OAOptions.objects.all().count())


class ApplOptionsTest(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.userProfile = UserProfileFactory(user=self.user)
        self.applType_prov = ApplTypeFactory(prov=True)
        self.applType_pct = ApplTypeFactory(pct=True)
        self.applType_utility = ApplTypeFactory(utility=True)
        self.applType_ep = ApplTypeFactory(ep=True)
        self.applType_epvalidation = ApplTypeFactory(epvalidation=True)
        self.applType_nationalphase = ApplTypeFactory(nationalphase=True)
        self.language_english = LanguagesFactory(english=True)
        self.language_chinese = LanguagesFactory(chinese=True)
        self.country_US = CountryFactory(US=True, languages=[self.language_english])
        self.country_CN = CountryFactory(CN=True, languages=[self.language_chinese])
        self.countries = [self.country_US, self.country_CN]

        self.entitySize = EntitySizeFactory()
        self.family = FamilyFactory(user=self.user)
        self.dfltFilTrans_prov = DefaultFilingTransformFactory(appl_type=self.applType_prov)
        self.dfltFilTrans_pct = DefaultFilingTransformFactory(appl_type=self.applType_pct)
        self.dfltFilTrans_utility = DefaultFilingTransformFactory(appl_type=self.applType_utility)
        self.defaultCountryOANum = DefaultCountryOANumFactory()
        self.dfltPublTrans_pct = DefaultPublTransformFactory(appl_type=self.applType_pct)
        self.dfltPublTrans_utility = DefaultPublTransformFactory(appl_type=self.applType_utility)
        self.dfltOATransform = DefaultOATransformFactory(appl_type=self.applType_utility)
        self.dfltAllowTransform = DefaultAllowanceTransformFactory()
        self.dfltIssueTransform = DefaultIssueTransformFactory(appl_type=self.applType_utility)

        self.customFilTrans = CustomFilingTransformFactory(appl_type=self.applType_prov,
                                                           prev_appl_type=None,
                                                           country=self.country_US)
        self.issTrans = IssueTransformFactory(country=self.country_US)
        self.allowTrans = AllowanceTransformFactory(country=self.country_US)
        self.oaTrans = OATransformFactory(country=self.country_US)
        self.publTrans = PublicationTransformFactory(country=self.country_US)
        self.countryOANum = CountryOANumFactory(country=self.country_US)

        self.famFormData = FamEstFormDataFactory(init_appl_country=self.country_US,
                                                 init_appl_type=self.applType_prov,
                                                 meth_country=self.country_US,
                                                 countries=self.countries)

        self.filing_template_us = FilingEstimateTemplateFactory(country=self.country_US,
                                                                appl_type=self.applType_utility)
        self.publication_template = PublicationEstTemplateFactory(country=self.country_US)
        self.oa_template = OAEstimateTemplateFactory(country=self.country_US)
        self.allowance_template = AllowanceEstTemplateFactory(country=self.country_US)
        self.issue_template = IssueEstTemplateFactory(country=self.country_US)
        self.applOption = ApplOptionsFactory()
        self.applOption_CN = ApplOptionsFactory(country=self.country_CN)
        # self.publOption = PublOptionFactory()



    def test_create_publ_option_creates_publOption(self):
        publOption = self.applOption.create_publ_option()
        self.assertEquals(publOption, PublOptions.objects.first())

    def test_create_publ_option_returns_default(self):
        publOption = self.applOption_CN.create_publ_option()
        self.assertEquals(publOption.date_diff, self.dfltPublTrans_utility.date_diff)

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
        self.assertEquals(oaOption.date_diff, self.oaTrans.date_diff)

    def test_create_oa_options_correct_length_3(self):
        oa_tot=3
        allOAOptions = self.applOption.create_all_oa_options(oa_tot=oa_tot)
        self.assertEquals(len(allOAOptions), OAOptions.objects.all().count())

    def test_create_oa_options_correct_length_1(self):
        oa_tot=1
        allOAOptions = self.applOption.create_all_oa_options(oa_tot=oa_tot)
        self.assertEquals(len(allOAOptions), OAOptions.objects.all().count())

