from datetime import date, datetime

from django.test import TestCase

from account.factories import UserProfileFactory
from application.factories import ApplDetailsFactory
from application.models import BaseApplication, Publication
from characteristics.enums import TranslationRequirements
from characteristics.factories import ApplTypeFactory, CountryFactory, EntitySizeFactory, LanguageFactory, \
    TotalCountryFactoryUS, TotalCountryFactoryCN, AvailableLanguagesFactory, TranslationImplementedPseudoEnumFactory, \
    AvailableApplTypesFactory, AvailableISACountriesFactory, TotalCountryFactoryGB, TotalCountryFactoryEP
from estimation.models import PublicationEstTemplate, PublicationEst
from family.factories import FamilyFactory
from transform.factories import DefaultFilingTransformFactory, CustomFilingTransformFactory, IssueTransformFactory, \
    AllowanceTransformFactory, OATransformFactory, PublicationTransformFactory, CountryOANumFactory, \
    DefaultCountryOANumFactory, DefaultPublTransformFactory, DefaultOATransformFactory, \
    DefaultAllowanceTransformFactory, DefaultIssueTransformFactory, RequestExaminationTransformFactory, \
    DefaultRequestExaminationTransformFactory
from transform.models import DefaultFilingTransform, DefaultOATransform
from .factories import FamEstFormDataFactory, ApplOptionsFactory, PublOptionFactory, FamOptionsFactory, \
    ApplOptionsParticularsFactory, OAOptionsFactory, AllowOptionsFactory, IssueOptionsFactory, CustomApplDetailsFactory, \
    CustomApplOptionsFactory, generate_paris_countries, ParisCountriesFactory, EPCountriesFactory, PCTCountriesFactory
from pestimator.exceptions import ApplTypePCTNotSupportedException, ApplTypePCTNationalPhaseNotSupportedException, \
    ApplTypeNotAvailableForCountry, ISACountryNotAvailableForCountry
from .models import ApplOptions, PublOptions, OAOptions, \
    AllowOptions, IssueOptions, RequestExaminationOptions, PCTApplOptions, FamOptions, ParisCountryCustomization, \
    EPCountryCustomization


class FamFormApplicationTest(TestCase):

    def setUp(self):
        country = CountryFactory(GB=True)
        country = CountryFactory(EP=True)
        appl_type = ApplTypeFactory(utility=True)
        appl_type_prov = ApplTypeFactory(prov=True)
        appl_type_pct = ApplTypeFactory(pct=True)
        appl_type_ep = ApplTypeFactory(ep=True)
        appl_type_epvalidation = ApplTypeFactory(epvalidation=True)
        oa_transform = OATransformFactory(country=country, appl_type=appl_type)
        date_filing = datetime(2020, 6, 4)
        language_en = LanguageFactory(name='English', words_per_page=100)
        language_cn = LanguageFactory(name='Chinese', words_per_page=700)
        language_de = LanguageFactory(name='Chinese', words_per_page=300)
        TranslationImplementedPseudoEnumFactory(no_translation=True)
        TranslationImplementedPseudoEnumFactory(full_translation=True)
        dfltOATrans = DefaultCountryOANumFactory(oa_total=2)
        dfltFilTrans = DefaultFilingTransformFactory(appl_type=appl_type)
        dfltPublTrans = DefaultPublTransformFactory(appl_type=appl_type)
        dfltReqExamTrans = DefaultRequestExaminationTransformFactory(appl_type=appl_type)
        dfltOATrans = DefaultOATransformFactory(appl_type=appl_type)
        dfltAllowTrans = DefaultAllowanceTransformFactory(appl_type=appl_type)
        dfltIssueTrans = DefaultIssueTransformFactory(appl_type=appl_type)
        dfltFilTrans = DefaultFilingTransformFactory(appl_type=appl_type_prov)
        dfltPublTrans = DefaultPublTransformFactory(appl_type=appl_type_prov)
        dfltReqExamTrans = DefaultRequestExaminationTransformFactory(appl_type=appl_type_prov)
        dfltOATrans = DefaultOATransformFactory(appl_type=appl_type_prov)
        dfltAllowTrans = DefaultAllowanceTransformFactory(appl_type=appl_type_prov)
        dfltIssueTrans = DefaultIssueTransformFactory(appl_type=appl_type_prov)
        dfltFilTrans = DefaultFilingTransformFactory(appl_type=appl_type_pct)
        dfltPublTrans = DefaultPublTransformFactory(appl_type=appl_type_pct)
        dfltReqExamTrans = DefaultRequestExaminationTransformFactory(appl_type=appl_type_pct)
        dfltOATrans = DefaultOATransformFactory(appl_type=appl_type_pct)
        dfltAllowTrans = DefaultAllowanceTransformFactory(appl_type=appl_type_pct)
        dfltIssueTrans = DefaultIssueTransformFactory(appl_type=appl_type_pct)
        dfltFilTrans = DefaultFilingTransformFactory(appl_type=appl_type_ep)
        dfltPublTrans = DefaultPublTransformFactory(appl_type=appl_type_ep)
        dfltReqExamTrans = DefaultRequestExaminationTransformFactory(appl_type=appl_type_ep)
        dfltOATrans = DefaultOATransformFactory(appl_type=appl_type_ep)
        dfltAllowTrans = DefaultAllowanceTransformFactory(appl_type=appl_type_ep)
        dfltIssueTrans = DefaultIssueTransformFactory(appl_type=appl_type_ep)
        dfltFilTrans = DefaultFilingTransformFactory(appl_type=appl_type_epvalidation)
        dfltPublTrans = DefaultPublTransformFactory(appl_type=appl_type_epvalidation)
        dfltReqExamTrans = DefaultRequestExaminationTransformFactory(appl_type=appl_type_epvalidation)
        dfltOATrans = DefaultOATransformFactory(appl_type=appl_type_epvalidation)
        dfltAllowTrans = DefaultAllowanceTransformFactory(appl_type=appl_type_epvalidation)
        dfltIssueTrans = DefaultIssueTransformFactory(appl_type=appl_type_epvalidation)

    def test_parse_first_appl_stage_returns_first_appl_option_prov(self):
        country_us = TotalCountryFactoryUS()
        appl_type = ApplTypeFactory(prov=True)
        family = FamilyFactory()
        fam_options = FamOptionsFactory(family=family)
        famForm = FamEstFormDataFactory(init_appl_type=appl_type, init_appl_country=country_us,
                                        family=family)
        appl_details = ApplDetailsFactory()

        appl_option = famForm.parse_first_appl_stage(famOptions=fam_options,
                                                     applDetails=appl_details)
        self.assertIsInstance(appl_option, ApplOptions)
        self.assertEquals(appl_option.appl_type, appl_type)

    def test_parse_first_appl_stage_returns_first_appl_option_pct(self):
        country_us = TotalCountryFactoryUS()
        country_cn = TotalCountryFactoryCN()
        # country_cn = CountryFactory(CN=True)
        appl_type = ApplTypeFactory(pct=True)
        famForm = FamEstFormDataFactory(init_appl_type=appl_type, pct_method=True, pct_country=country_us,
                                        init_appl_country=country_us)
        fam_options = FamOptionsFactory()
        appl_details = ApplDetailsFactory()
        appl_option = famForm.parse_first_appl_stage(famOptions=fam_options,
                                                     applDetails=appl_details)
        self.assertIsInstance(appl_option, PCTApplOptions)
        self.assertEquals(appl_option.appl_type, appl_type)

    def test_parse_first_appl_stage_returns_first_appl_option_ep(self):
        # country_us = TotalCountryFactoryUS()
        country_gb = TotalCountryFactoryGB()
        country_ep = TotalCountryFactoryEP()
        # country_cn = TotalCountryFactoryCN()
        appl_type = ApplTypeFactory(ep=True)
        famForm = FamEstFormDataFactory(init_appl_type=appl_type,
                                        pct_method=False,
                                        ep_method=True,
                                        init_appl_country=country_ep)
        fam_options = FamOptionsFactory()
        appl_details = ApplDetailsFactory()
        appl_option = famForm.parse_first_appl_stage(famOptions=fam_options,
                                                     applDetails=appl_details)
        self.assertIsInstance(appl_option, ApplOptions)
        self.assertEquals(appl_option.appl_type, appl_type)

    def test_parse_paris_stage_return_init_appl_option_with_children_appl_options(self):
        country_us = TotalCountryFactoryUS()
        country_gb = TotalCountryFactoryGB()
        # country_ep = TotalCountryFactoryEP()
        country_cn = TotalCountryFactoryCN()
        appl_type = ApplTypeFactory(utility=True)
        famForm = FamEstFormDataFactory(init_appl_type=appl_type,
                                        pct_method=False,
                                        ep_method=False,
                                        init_appl_country=country_us)
        fam_options = FamOptionsFactory()
        appl_details = ApplDetailsFactory()
        firstApplOption = ApplOptionsFactory(country=country_us)
        ParisCountryCustomization.objects.all().delete()
        ParisCountriesFactory(
            fam_est_form_data=famForm,
            country=country_gb)
        ParisCountriesFactory(
            fam_est_form_data=famForm,
            country=country_cn,
        )
        appl_option = famForm.parse_paris_stage(famOptions=fam_options,
                                                prevApplOption=firstApplOption,
                                                applDetails=appl_details)

        self.assertIsInstance(appl_option, ApplOptions)
        self.assertEquals(appl_option.appl_type, appl_type)
        self.assertEquals(appl_option.apploptions_set.count(), 2)
        self.assertTrue(appl_option.apploptions_set.filter(country=country_gb).exists())
        self.assertTrue(appl_option.apploptions_set.filter(country=country_cn).exists())

    def test_parse_paris_stage_return_init_appl_option_with_children_appl_options_ep_method_true(self):
        country_us = TotalCountryFactoryUS()
        country_gb = TotalCountryFactoryGB()
        country_ep = TotalCountryFactoryEP()
        country_cn = TotalCountryFactoryCN()
        appl_type = ApplTypeFactory(utility=True)
        famForm = FamEstFormDataFactory(init_appl_type=appl_type,
                                        pct_method=False,
                                        ep_method=True,
                                        init_appl_country=country_us)
        fam_options = FamOptionsFactory()
        appl_details = ApplDetailsFactory()
        firstApplOption = ApplOptionsFactory(country=country_us)
        ParisCountryCustomization.objects.all().delete()
        EPCountryCustomization.objects.all().delete()
        EPCountriesFactory(
            fam_est_form_data=famForm,
            country=country_gb)
        ParisCountriesFactory(
            fam_est_form_data=famForm,
            country=country_ep)
        ParisCountriesFactory(
            fam_est_form_data=famForm,
            country=country_cn,
        )
        appl_option = famForm.parse_paris_stage(famOptions=fam_options,
                                                prevApplOption=firstApplOption,
                                                applDetails=appl_details)

        self.assertIsInstance(appl_option, ApplOptions)
        self.assertEquals(appl_option.appl_type, appl_type)
        self.assertEquals(appl_option.apploptions_set.count(), 2)
        self.assertTrue(appl_option.apploptions_set.filter(country=country_ep).exists())
        self.assertTrue(appl_option.apploptions_set.filter(country=country_cn).exists())
        ep_appl_option = appl_option.apploptions_set.get(country=country_ep)
        self.assertTrue(ep_appl_option.apploptions_set.filter(country=country_gb).exists())

    def test_parse_ep_stage_returns_appl_option_with_children_appl_options(self):
        country_us = TotalCountryFactoryUS()
        country_gb = TotalCountryFactoryGB()
        country_ep = TotalCountryFactoryEP()
        # country_cn = TotalCountryFactoryCN()
        appl_type = ApplTypeFactory(ep=True)
        appl_type_utility = ApplTypeFactory(utility=True)
        famForm = FamEstFormDataFactory(init_appl_type=appl_type,
                                        pct_method=False,
                                        ep_method=True,
                                        init_appl_country=country_us)
        fam_options = FamOptionsFactory()
        appl_details = ApplDetailsFactory()
        firstApplOption = ApplOptionsFactory(country=country_us)
        EPCountryCustomization.objects.all().delete()
        EPCountriesFactory(
            fam_est_form_data=famForm,
            country=country_gb)
        appl_option = famForm.parse_ep_stage(famOptions=fam_options,
                                             firstApplBool=False,
                                             prev_date=datetime(2015, 1, 23),
                                             prev_appl_type=appl_type_utility,
                                             prevApplOption=firstApplOption,
                                             applDetails=appl_details)

        self.assertIsInstance(appl_option, ApplOptions)
        self.assertEquals(appl_option.appl_type, appl_type)
        self.assertEquals(appl_option.apploptions_set.count(), 1)
        self.assertTrue(appl_option.apploptions_set.filter(country=country_gb).exists())

    def test_parse_ep_validateion_stage_returns_ep_appl_option_with_children_appl_options(self):
        country_us = TotalCountryFactoryUS()
        country_gb = TotalCountryFactoryGB()
        country_ep = TotalCountryFactoryEP()
        # country_cn = TotalCountryFactoryCN()
        appl_type = ApplTypeFactory(ep=True)
        appl_type_epvalid = ApplTypeFactory(epvalidation=True)
        appl_type_utility = ApplTypeFactory(utility=True)
        famForm = FamEstFormDataFactory(init_appl_type=appl_type,
                                        pct_method=False,
                                        ep_method=True,
                                        init_appl_country=country_us)
        fam_options = FamOptionsFactory()
        appl_details = ApplDetailsFactory()
        DefaultOATransform.objects.filter(appl_type=appl_type).delete()
        dfltOATrans = DefaultOATransformFactory(appl_type=appl_type, date_diff='P1Y')
        firstApplOption = ApplOptionsFactory(country=country_ep, appl_type=appl_type)
        oa_options = OAOptionsFactory(appl=firstApplOption)
        allow_options = AllowOptionsFactory(appl=firstApplOption)
        EPCountryCustomization.objects.all().delete()
        EPCountriesFactory(
            fam_est_form_data=famForm,
            country=country_gb)
        appl_option = famForm.parse_ep_validation_stage(
            famOptions=fam_options,
            prevApplOption=firstApplOption,
            applDetails=appl_details)

        self.assertIsInstance(appl_option, ApplOptions)
        self.assertEquals(appl_option.appl_type, appl_type)
        self.assertEquals(appl_option.apploptions_set.count(), 1)
        self.assertTrue(appl_option.apploptions_set.filter(country=country_gb).exists())
        ep_prev_date = appl_option.date_filing + (
            oa_options.date_diff) + allow_options.date_diff + DefaultFilingTransform.objects.get(
            appl_type=appl_type_epvalid).date_diff
        self.assertEquals(ep_prev_date, ApplOptions.objects.get(appl_type=appl_type_epvalid).date_filing)

    def test_parse_international_stage_returns_pct_appl_options_with_appropriate_children(self):
        country_us = TotalCountryFactoryUS()
        country_gb = TotalCountryFactoryGB()
        # country_ep = TotalCountryFactoryEP()
        country_cn = TotalCountryFactoryCN()
        appl_type = ApplTypeFactory(ep=True)
        appl_type_pct = ApplTypeFactory(pct=True)
        appl_type_epvalid = ApplTypeFactory(epvalidation=True)
        appl_type_utility = ApplTypeFactory(utility=True)
        famForm = FamEstFormDataFactory(init_appl_type=appl_type_pct,
                                        pct_method=True,
                                        pct_country=country_us,
                                        isa_country=country_us,
                                        ep_method=False,
                                        init_appl_country=country_us)
        fam_options = FamOptionsFactory()
        appl_details = ApplDetailsFactory()
        # DefaultOATransform.objects.filter(appl_type=appl_type).delete()
        firstApplOption = ApplOptionsFactory(country=country_us, appl_type=appl_type_utility)
        oa_options = OAOptionsFactory(appl=firstApplOption)
        allow_options = AllowOptionsFactory(appl=firstApplOption)
        EPCountryCustomization.objects.all().delete()
        PCTCountriesFactory(
            fam_est_form_data=famForm,
            country=country_gb)
        PCTCountriesFactory(
            fam_est_form_data=famForm,
            country=country_cn)
        appl_option = famForm.parse_international_stage(
            famOptions=fam_options,
            prevDate=datetime(2014, 9, 1),
            prevApplType=appl_type_utility,
            firstApplBool=False,
            prevApplOption=firstApplOption,
            applDetails=appl_details)

        self.assertIsInstance(appl_option, ApplOptions)
        self.assertEquals(appl_option.appl_type, appl_type_pct)
        self.assertEquals(appl_option.apploptions_set.count(), 2)
        self.assertTrue(appl_option.apploptions_set.filter(country=country_gb).exists())
        self.assertTrue(appl_option.apploptions_set.filter(country=country_cn).exists())
        ep_prev_date = appl_option.date_filing + DefaultFilingTransform.objects.get(
            appl_type=appl_type_utility).date_diff
        self.assertEquals(ep_prev_date.date(), appl_option.apploptions_set.get(country=country_cn).date_filing)

    def test_generate_family_options_creates_first_appl(self):
        self.fail('Add Tests for Generate Family Options good Launch point for integration tests')


class FamOptionsTest(TestCase):

    def test_generate_pct_appl_returns_appl_option_with_custom_details(self):
        country = CountryFactory(GB=True)
        appl_type = ApplTypeFactory(pct=True)
        oa_transform = OATransformFactory(country=country, appl_type=appl_type)
        date_filing = datetime(2020, 6, 4)
        language_en = LanguageFactory(name='English', words_per_page=100)
        language_cn = LanguageFactory(name='Chinese', words_per_page=700)
        language_de = LanguageFactory(name='Chinese', words_per_page=300)
        dfltOATrans = DefaultCountryOANumFactory(oa_total=2)
        dfltFilTrans = DefaultFilingTransformFactory(appl_type=appl_type)
        dfltPublTrans = DefaultPublTransformFactory(appl_type=appl_type)
        dfltReqExamTrans = DefaultRequestExaminationTransformFactory(appl_type=appl_type)
        dfltOATrans = DefaultOATransformFactory(appl_type=appl_type)
        dfltAllowTrans = DefaultAllowanceTransformFactory(appl_type=appl_type)
        dfltIssueTrans = DefaultIssueTransformFactory(appl_type=appl_type)
        details = ApplDetailsFactory(language=language_cn, num_pages_description=12)
        custom_details = CustomApplDetailsFactory(language=language_de)
        custom_options = CustomApplOptionsFactory()
        prev_appl_type = None
        prev_date = datetime(2004, 1, 2)
        first_appl_bool = True
        country_cn = CountryFactory(CN=True)
        prev_appl_option = ApplOptionsFactory(country=country_cn, details=details)
        fam_option = FamOptionsFactory()
        particulars = ApplOptionsParticularsFactory()
        AvailableLanguagesFactory(language=language_en, country=country, appl_type=appl_type)
        AvailableApplTypesFactory(country=country, appltype=appl_type)
        TranslationImplementedPseudoEnumFactory(no_translation=True)
        TranslationImplementedPseudoEnumFactory(full_translation=True)
        AvailableISACountriesFactory(from_country=country, to_country=country)
        returned_appl_option = fam_option.generate_pct_appl(
            details=details,
            custom_details=custom_details,
            country=country,
            isa_country=country,
            custom_options=custom_options,
            prev_appl_type=prev_appl_type,
            prev_date=prev_date,
            first_appl_bool=first_appl_bool,
            prev_appl_option=prev_appl_option)
        self.assertEquals(returned_appl_option.details.num_pages_description, custom_details.num_pages_description)
        self.assertEquals(returned_appl_option.details.num_pages_drawings, custom_details.num_pages_drawings)
        self.assertEquals(returned_appl_option.details.num_pages_claims, custom_details.num_pages_claims)
        self.assertEquals(returned_appl_option.details.num_claims, custom_details.num_claims)
        self.assertEquals(returned_appl_option.details.num_indep_claims, custom_details.num_indep_claims)
        self.assertEquals(returned_appl_option.details.num_claims_multiple_dependent,
                          custom_details.num_claims_multiple_dependent)
        self.assertEquals(returned_appl_option.details.entity_size, custom_details.entity_size)
        self.assertEquals(returned_appl_option.details.language, custom_details.language)

    def test_generate_pct_appl_returns_appl_option_with_translated_details(self):
        country = CountryFactory(GB=True)
        appl_type = ApplTypeFactory(pct=True)
        oa_transform = OATransformFactory(country=country, appl_type=appl_type)
        date_filing = datetime(2020, 6, 4)
        language_en = LanguageFactory(name='English', words_per_page=100)
        language_cn = LanguageFactory(name='Chinese', words_per_page=700)
        dfltOATrans = DefaultCountryOANumFactory(oa_total=2)
        dfltFilTrans = DefaultFilingTransformFactory(appl_type=appl_type)
        dfltPublTrans = DefaultPublTransformFactory(appl_type=appl_type)
        dfltReqExamTrans = DefaultRequestExaminationTransformFactory(appl_type=appl_type)
        dfltOATrans = DefaultOATransformFactory(appl_type=appl_type)
        dfltAllowTrans = DefaultAllowanceTransformFactory(appl_type=appl_type)
        dfltIssueTrans = DefaultIssueTransformFactory(appl_type=appl_type)
        details = ApplDetailsFactory(language=language_cn, num_pages_description=12)
        custom_details = CustomApplDetailsFactory(NONE=True)
        custom_options = CustomApplOptionsFactory()
        prev_appl_type = None
        prev_date = datetime(2004, 1, 2)
        first_appl_bool = True
        country_cn = CountryFactory(CN=True)
        prev_appl_option = ApplOptionsFactory(country=country_cn, details=details)
        fam_option = FamOptionsFactory()
        particulars = ApplOptionsParticularsFactory()
        AvailableLanguagesFactory(language=language_en, country=country, appl_type=appl_type)
        AvailableApplTypesFactory(country=country, appltype=appl_type)
        TranslationImplementedPseudoEnumFactory(no_translation=True)
        TranslationImplementedPseudoEnumFactory(full_translation=True)
        AvailableISACountriesFactory(from_country=country, to_country=country)
        returned_appl_option = fam_option.generate_pct_appl(
            details=details,
            custom_details=custom_details,
            country=country,
            isa_country=country,
            custom_options=custom_options,
            prev_appl_type=prev_appl_type,
            prev_date=prev_date,
            first_appl_bool=first_appl_bool,
            prev_appl_option=prev_appl_option)
        self.assertEquals(returned_appl_option.details.num_pages_description, 84)

    def test_generate_pct_appl_returns_appl_option_with_children_for_utility_appl_type(self):
        country = CountryFactory(GB=True)
        appl_type = ApplTypeFactory(pct=True)
        oa_transform = OATransformFactory(country=country, appl_type=appl_type)
        date_filing = datetime(2020, 6, 4)
        language_cn = LanguageFactory(Chinese=True)
        dfltOATrans = DefaultCountryOANumFactory(oa_total=2)
        dfltFilTrans = DefaultFilingTransformFactory(appl_type=appl_type)
        dfltPublTrans = DefaultPublTransformFactory(appl_type=appl_type)
        dfltReqExamTrans = DefaultRequestExaminationTransformFactory(appl_type=appl_type)
        dfltOATrans = DefaultOATransformFactory(appl_type=appl_type)
        dfltAllowTrans = DefaultAllowanceTransformFactory(appl_type=appl_type)
        dfltIssueTrans = DefaultIssueTransformFactory(appl_type=appl_type)
        details = ApplDetailsFactory(language=language_cn)
        custom_details = CustomApplDetailsFactory()
        custom_options = CustomApplOptionsFactory()
        prev_appl_type = None
        prev_date = datetime(2004, 1, 2)
        first_appl_bool = True
        prev_appl_option = None
        fam_option = FamOptionsFactory()
        particulars = ApplOptionsParticularsFactory()
        AvailableApplTypesFactory(country=country, appltype=appl_type)
        AvailableISACountriesFactory(from_country=country, to_country=country)
        TranslationImplementedPseudoEnumFactory(no_translation=True)
        TranslationImplementedPseudoEnumFactory(full_translation=True)
        returned_appl_option = fam_option.generate_pct_appl(
            details=details,
            custom_details=custom_details,
            country=country,
            isa_country=country,
            custom_options=custom_options,
            prev_appl_type=prev_appl_type,
            prev_date=prev_date,
            first_appl_bool=first_appl_bool,
            prev_appl_option=prev_appl_option)
        self.assertTrue(hasattr(returned_appl_option, 'publoptions'))
        self.assertTrue(hasattr(returned_appl_option, 'requestexaminationoptions'))
        self.assertEquals(returned_appl_option.oaoptions_set.count(), 2)
        self.assertFalse(hasattr(returned_appl_option, 'allowoptions'))
        self.assertFalse(hasattr(returned_appl_option, 'issueoptions'))

    def test_generate_pct_appl_raises_appl_type_not_available_exception(self):
        country = CountryFactory(GB=True)
        appl_type = ApplTypeFactory(utility=True)
        appl_type_pct = ApplTypeFactory(pct=True)
        appl_type_ep = ApplTypeFactory(ep=True)
        oa_transform = OATransformFactory(country=country, appl_type=appl_type)
        date_filing = datetime(2020, 6, 4)
        language_cn = LanguageFactory(Chinese=True)
        dfltOATrans = DefaultCountryOANumFactory(oa_total=2)
        dfltFilTrans = DefaultFilingTransformFactory(appl_type=appl_type)
        dfltPublTrans = DefaultPublTransformFactory(appl_type=appl_type)
        dfltReqExamTrans = DefaultRequestExaminationTransformFactory(appl_type=appl_type)
        dfltOATrans = DefaultOATransformFactory(appl_type=appl_type)
        dfltAllowTrans = DefaultAllowanceTransformFactory(appl_type=appl_type)
        dfltIssueTrans = DefaultIssueTransformFactory(appl_type=appl_type)
        details = ApplDetailsFactory(language=language_cn)
        custom_details = CustomApplDetailsFactory()
        custom_options = CustomApplOptionsFactory()
        prev_appl_type = None
        prev_date = datetime(2004, 1, 2)
        first_appl_bool = True
        prev_appl_option = None
        fam_option = FamOptionsFactory()
        particulars = ApplOptionsParticularsFactory()
        AvailableApplTypesFactory(country=country, appltype=appl_type)

        self.assertRaises(ISACountryNotAvailableForCountry,
                          fam_option.generate_pct_appl,
                          details=details,
                          custom_details=custom_details,
                          country=country,
                          isa_country=country,
                          custom_options=custom_options,
                          prev_appl_type=prev_appl_type,
                          prev_date=prev_date,
                          first_appl_bool=first_appl_bool,
                          prev_appl_option=prev_appl_option)

    # *****************************************************

    def test_generate_appl_returns_appl_option_with_custom_details(self):
        country = CountryFactory(GB=True)
        appl_type = ApplTypeFactory(utility=True)
        oa_transform = OATransformFactory(country=country, appl_type=appl_type)
        date_filing = datetime(2020, 6, 4)
        language_en = LanguageFactory(name='English', words_per_page=100)
        language_cn = LanguageFactory(name='Chinese', words_per_page=700)
        language_de = LanguageFactory(name='Chinese', words_per_page=300)
        dfltOATrans = DefaultCountryOANumFactory(oa_total=2)
        dfltFilTrans = DefaultFilingTransformFactory(appl_type=appl_type)
        dfltPublTrans = DefaultPublTransformFactory(appl_type=appl_type)
        dfltReqExamTrans = DefaultRequestExaminationTransformFactory(appl_type=appl_type)
        dfltOATrans = DefaultOATransformFactory(appl_type=appl_type)
        dfltAllowTrans = DefaultAllowanceTransformFactory(appl_type=appl_type)
        dfltIssueTrans = DefaultIssueTransformFactory(appl_type=appl_type)
        details = ApplDetailsFactory(language=language_cn, num_pages_description=12)
        custom_details = CustomApplDetailsFactory(language=language_de)
        custom_options = CustomApplOptionsFactory()
        prev_appl_type = None
        prev_date = datetime(2004, 1, 2)
        first_appl_bool = True
        country_cn = CountryFactory(CN=True)
        prev_appl_option = ApplOptionsFactory(country=country_cn, details=details)
        fam_option = FamOptionsFactory()
        particulars = ApplOptionsParticularsFactory()
        AvailableLanguagesFactory(language=language_en, country=country, appl_type=appl_type)
        AvailableApplTypesFactory(country=country, appltype=appl_type)
        TranslationImplementedPseudoEnumFactory(no_translation=True)
        TranslationImplementedPseudoEnumFactory(full_translation=True)
        returned_appl_option = fam_option.generate_appl(
            details=details,
            custom_details=custom_details,
            country=country,
            appl_type=appl_type,
            custom_options=custom_options,
            prev_appl_type=prev_appl_type,
            prev_date=prev_date,
            first_appl_bool=first_appl_bool,
            prev_appl_option=prev_appl_option)
        self.assertEquals(returned_appl_option.details.num_pages_description, custom_details.num_pages_description)
        self.assertEquals(returned_appl_option.details.num_pages_drawings, custom_details.num_pages_drawings)
        self.assertEquals(returned_appl_option.details.num_pages_claims, custom_details.num_pages_claims)
        self.assertEquals(returned_appl_option.details.num_claims, custom_details.num_claims)
        self.assertEquals(returned_appl_option.details.num_indep_claims, custom_details.num_indep_claims)
        self.assertEquals(returned_appl_option.details.num_claims_multiple_dependent,
                          custom_details.num_claims_multiple_dependent)
        self.assertEquals(returned_appl_option.details.entity_size, custom_details.entity_size)
        self.assertEquals(returned_appl_option.details.language, custom_details.language)

    def test_generate_appl_returns_appl_option_with_translated_details(self):
        country = CountryFactory(GB=True)
        appl_type = ApplTypeFactory(utility=True)
        oa_transform = OATransformFactory(country=country, appl_type=appl_type)
        date_filing = datetime(2020, 6, 4)
        language_en = LanguageFactory(name='English', words_per_page=100)
        language_cn = LanguageFactory(name='Chinese', words_per_page=700)
        dfltOATrans = DefaultCountryOANumFactory(oa_total=2)
        dfltFilTrans = DefaultFilingTransformFactory(appl_type=appl_type)
        dfltPublTrans = DefaultPublTransformFactory(appl_type=appl_type)
        dfltReqExamTrans = DefaultRequestExaminationTransformFactory(appl_type=appl_type)
        dfltOATrans = DefaultOATransformFactory(appl_type=appl_type)
        dfltAllowTrans = DefaultAllowanceTransformFactory(appl_type=appl_type)
        dfltIssueTrans = DefaultIssueTransformFactory(appl_type=appl_type)
        details = ApplDetailsFactory(language=language_cn, num_pages_description=12)
        custom_details = CustomApplDetailsFactory(NONE=True)
        custom_options = CustomApplOptionsFactory()
        prev_appl_type = None
        prev_date = datetime(2004, 1, 2)
        first_appl_bool = True
        country_cn = CountryFactory(CN=True)
        prev_appl_option = ApplOptionsFactory(country=country_cn, details=details)
        fam_option = FamOptionsFactory()
        particulars = ApplOptionsParticularsFactory()
        AvailableLanguagesFactory(language=language_en, country=country, appl_type=appl_type)
        AvailableApplTypesFactory(country=country, appltype=appl_type)
        TranslationImplementedPseudoEnumFactory(no_translation=True)
        TranslationImplementedPseudoEnumFactory(full_translation=True)
        returned_appl_option = fam_option.generate_appl(
            details=details,
            custom_details=custom_details,
            country=country,
            appl_type=appl_type,
            custom_options=custom_options,
            prev_appl_type=prev_appl_type,
            prev_date=prev_date,
            first_appl_bool=first_appl_bool,
            prev_appl_option=prev_appl_option)
        self.assertEquals(returned_appl_option.details.num_pages_description, 84)

    def test_generate_appl_returns_appl_option_with_children_for_utility_appl_type(self):
        country = CountryFactory(GB=True)
        appl_type = ApplTypeFactory(utility=True)
        oa_transform = OATransformFactory(country=country, appl_type=appl_type)
        date_filing = datetime(2020, 6, 4)
        language_cn = LanguageFactory(Chinese=True)
        dfltOATrans = DefaultCountryOANumFactory(oa_total=2)
        dfltFilTrans = DefaultFilingTransformFactory(appl_type=appl_type)
        dfltPublTrans = DefaultPublTransformFactory(appl_type=appl_type)
        dfltReqExamTrans = DefaultRequestExaminationTransformFactory(appl_type=appl_type)
        dfltOATrans = DefaultOATransformFactory(appl_type=appl_type)
        dfltAllowTrans = DefaultAllowanceTransformFactory(appl_type=appl_type)
        dfltIssueTrans = DefaultIssueTransformFactory(appl_type=appl_type)
        details = ApplDetailsFactory(language=language_cn)
        custom_details = CustomApplDetailsFactory()
        custom_options = CustomApplOptionsFactory()
        prev_appl_type = None
        prev_date = datetime(2004, 1, 2)
        first_appl_bool = True
        prev_appl_option = None
        fam_option = FamOptionsFactory()
        particulars = ApplOptionsParticularsFactory()
        AvailableApplTypesFactory(country=country, appltype=appl_type)
        TranslationImplementedPseudoEnumFactory(no_translation=True)
        TranslationImplementedPseudoEnumFactory(full_translation=True)
        returned_appl_option = fam_option.generate_appl(
            details=details,
            custom_details=custom_details,
            country=country,
            appl_type=appl_type,
            custom_options=custom_options,
            prev_appl_type=prev_appl_type,
            prev_date=prev_date,
            first_appl_bool=first_appl_bool,
            prev_appl_option=prev_appl_option)
        self.assertTrue(hasattr(returned_appl_option, 'publoptions'))
        self.assertTrue(hasattr(returned_appl_option, 'requestexaminationoptions'))
        self.assertEquals(returned_appl_option.oaoptions_set.count(), 2)
        self.assertTrue(hasattr(returned_appl_option, 'allowoptions'))
        self.assertTrue(hasattr(returned_appl_option, 'issueoptions'))

    def test_generate_appl_raises_appl_type_not_available_exception(self):
        country = CountryFactory(GB=True)
        appl_type = ApplTypeFactory(utility=True)
        appl_type_ep = ApplTypeFactory(ep=True)
        oa_transform = OATransformFactory(country=country, appl_type=appl_type)
        date_filing = datetime(2020, 6, 4)
        language_cn = LanguageFactory(Chinese=True)
        dfltOATrans = DefaultCountryOANumFactory(oa_total=2)
        dfltFilTrans = DefaultFilingTransformFactory(appl_type=appl_type)
        dfltPublTrans = DefaultPublTransformFactory(appl_type=appl_type)
        dfltReqExamTrans = DefaultRequestExaminationTransformFactory(appl_type=appl_type)
        dfltOATrans = DefaultOATransformFactory(appl_type=appl_type)
        dfltAllowTrans = DefaultAllowanceTransformFactory(appl_type=appl_type)
        dfltIssueTrans = DefaultIssueTransformFactory(appl_type=appl_type)
        details = ApplDetailsFactory(language=language_cn)
        custom_details = CustomApplDetailsFactory()
        custom_options = CustomApplOptionsFactory()
        prev_appl_type = None
        prev_date = datetime(2004, 1, 2)
        first_appl_bool = True
        prev_appl_option = None
        fam_option = FamOptionsFactory()
        particulars = ApplOptionsParticularsFactory()
        AvailableApplTypesFactory(country=country, appltype=appl_type)

        self.assertRaises(ApplTypeNotAvailableForCountry,
                          fam_option.generate_appl,
                          details=details,
                          custom_details=custom_details,
                          country=country,
                          appl_type=appl_type_ep,
                          custom_options=custom_options,
                          prev_appl_type=prev_appl_type,
                          prev_date=prev_date,
                          first_appl_bool=first_appl_bool,
                          prev_appl_option=prev_appl_option)

    def test_smart_translate_details_no_custom_details_same_country(self):
        country = TotalCountryFactoryCN()
        language_cn = LanguageFactory(Chinese=True, words_per_page=500)
        details = ApplDetailsFactory(language=language_cn)
        appl_type = ApplTypeFactory(utility=True)
        appl_type_pct = ApplTypeFactory(pct=True)
        custom_details = None
        prev_appl_option = ApplOptionsFactory(appl_type=appl_type_pct, details=details)
        family_option = FamOptionsFactory()
        return_obj = family_option._smart_translate_details(
            country=country,
            details=details,
            appl_type=appl_type,
            custom_details=custom_details,
            prev_appl_option=prev_appl_option)

        self.assertEquals(return_obj['translated_details'].num_indep_claims, details.num_indep_claims)
        self.assertEquals(return_obj['translated_details'].num_claims, details.num_claims)
        self.assertEquals(return_obj['translated_details'].num_claims_multiple_dependent,
                          details.num_claims_multiple_dependent)
        self.assertEquals(return_obj['translated_details'].num_drawings, details.num_drawings)
        self.assertEquals(return_obj['translated_details'].num_pages_claims, details.num_pages_claims)
        self.assertEquals(return_obj['translated_details'].num_pages_description, details.num_pages_description)
        self.assertEquals(return_obj['translated_details'].num_pages_drawings, details.num_pages_drawings)
        self.assertEquals(return_obj['translated_details'].entity_size, details.entity_size)
        self.assertEquals(return_obj['translated_details'].language_id, details.language_id)
        self.assertEquals(return_obj['translation_enum'], TranslationRequirements.NO_TRANSLATION)

    def test_smart_translate_details_new_language_in_custom_options(self):
        language_cn = LanguageFactory(Chinese=True, words_per_page=500)
        language_en = LanguageFactory(English=True, words_per_page=100)
        country = TotalCountryFactoryCN()
        details = ApplDetailsFactory(language=language_cn, num_pages_description=10)
        appl_type = ApplTypeFactory(utility=True)
        appl_type_pct = ApplTypeFactory(pct=True)
        custom_details = CustomApplDetailsFactory(language=language_en)

        prev_appl_option = ApplOptionsFactory(appl_type=appl_type_pct,
                                              details=details)
        family_option = FamOptionsFactory()
        return_obj = family_option._smart_translate_details(
            country=country,
            details=details,
            appl_type=appl_type,
            custom_details=custom_details,
            prev_appl_option=prev_appl_option)

        self.assertEquals(return_obj['translated_details'].num_pages_description, details.num_pages_description * 5)
        self.assertEquals(return_obj['translated_details'].language_id, language_en.id)
        self.assertEquals(return_obj['translation_enum'], TranslationRequirements.FULL_TRANSLATION)

    def test_smart_translate_details_new_language_when_new_country_selected(self):
        language_cn = LanguageFactory(Chinese=True, words_per_page=100)
        language_en = LanguageFactory(English=True, words_per_page=500)
        country = TotalCountryFactoryCN()
        country_us = TotalCountryFactoryUS()
        # details = ApplDetailsFactory(language=language_cn, num_pages_description=10)
        details_us = ApplDetailsFactory(language=language_en, num_pages_description=10)
        appl_type = ApplTypeFactory(utility=True)
        appl_type_pct = ApplTypeFactory(pct=True)
        custom_details = None

        prev_appl_option = ApplOptionsFactory(
            country=country_us,
            appl_type=appl_type_pct,
            details=details_us)
        family_option = FamOptionsFactory()
        return_obj = family_option._smart_translate_details(
            country=country,
            details=details_us,
            appl_type=appl_type,
            custom_details=custom_details,
            prev_appl_option=prev_appl_option)

        self.assertEquals(return_obj['translated_details'].num_pages_description, details_us.num_pages_description * 5)
        self.assertEquals(return_obj['translated_details'].language_id, language_cn.id)
        self.assertEquals(return_obj['translation_enum'], TranslationRequirements.FULL_TRANSLATION)

    def test_translate_details_new_language_translates_num_pages(self):
        current_language = LanguageFactory(name='English', words_per_page=500)
        desired_language = LanguageFactory(name='Chinese', words_per_page=100)
        details = ApplDetailsFactory(num_pages_description=10)
        family_option = FamOptionsFactory()
        new_details = family_option.translate_details_new_language(details=details,
                                                                   current_language=current_language,
                                                                   desired_language=desired_language)
        self.assertEquals(new_details.num_pages_description, details.num_pages_description * 5)

    def test_translate_details_new_language_translates_num_pages_short_to_verbose(self):
        current_language = LanguageFactory(name='English', words_per_page=100)
        desired_language = LanguageFactory(name='Chinese', words_per_page=700)
        details = ApplDetailsFactory(num_pages_description=10)
        family_option = FamOptionsFactory()
        new_details = family_option.translate_details_new_language(details=details,
                                                                   current_language=current_language,
                                                                   desired_language=desired_language)
        self.assertEquals(new_details.num_pages_description, 2)

    def test_translate_details_new_language_translates_only_changes_num_pages(self):
        current_language = LanguageFactory(name='English', words_per_page=100)
        desired_language = LanguageFactory(name='Chinese', words_per_page=700)
        details = ApplDetailsFactory(num_pages_description=10)
        family_option = FamOptionsFactory()
        new_details = family_option.translate_details_new_language(details=details,
                                                                   current_language=current_language,
                                                                   desired_language=desired_language)
        self.assertEquals(new_details.num_indep_claims, details.num_indep_claims)
        self.assertEquals(new_details.num_claims, details.num_claims)
        self.assertEquals(new_details.num_claims_multiple_dependent, details.num_claims_multiple_dependent)
        self.assertEquals(new_details.num_drawings, details.num_drawings)
        self.assertEquals(new_details.num_pages_claims, details.num_pages_claims)
        self.assertEquals(new_details.num_pages_drawings, details.num_pages_drawings)
        self.assertEquals(new_details.entity_size, details.entity_size)
        self.assertNotEquals(new_details.language_id, details.language_id)

    def test_calc_filing_date_returns_date(self):
        country_us = CountryFactory(US=True)
        appl_type = ApplTypeFactory(utility=True)
        family_option = FamOptionsFactory()
        dfltFilTrans = DefaultFilingTransformFactory()
        prev_date = datetime(2020, 5, 27)
        date = family_option._calc_filing_date(appl_type, country_us, None,
                                               prev_date, None)
        self.assertIsInstance(date, datetime)

    def test_calc_oa_num_returns_CountryOANum(self):
        country_US = CountryFactory(US=True)
        appl_type = ApplTypeFactory()
        country_oa_num = CountryOANumFactory(country=country_US)
        family_option = FamOptionsFactory()
        oa_total = family_option._calc_oa_num(country_US, appl_type)
        self.assertEquals(oa_total, country_oa_num.oa_total)

    def test_calc_oa_num_returns_DefaultCountryOANum(self):
        country_CN = CountryFactory(CN=True)
        country_US = CountryFactory(US=True)
        appl_type = ApplTypeFactory()
        country_oa_num = CountryOANumFactory(country=country_US)
        default_country_oa_num = DefaultCountryOANumFactory()
        family_option = FamOptionsFactory()
        oa_total = family_option._calc_oa_num(country_CN, appl_type)
        self.assertEquals(oa_total, default_country_oa_num.oa_total)

    def test_apply_custom_details_empty_custom_details(self):
        translated_details = ApplDetailsFactory()
        custom_details = CustomApplDetailsFactory(NONE=True)
        family_option = FamOptionsFactory()
        final_details = family_option.apply_custom_details(translated_details, custom_details)
        self.assertEquals(translated_details, final_details)

    def test_apply_custom_details_num_claims_from_custom_details(self):
        translated_details = ApplDetailsFactory(num_claims=4)
        custom_details = CustomApplDetailsFactory(NUM_CLAIMS=True)
        family_option = FamOptionsFactory()
        final_details = family_option.apply_custom_details(translated_details, custom_details)
        self.assertNotEquals(translated_details.num_claims, final_details.num_claims)
        self.assertEquals(custom_details.num_claims, final_details.num_claims)

    def test_determine_desired_language_returns_language_as_custom_lang(self):
        translated_details = ApplDetailsFactory(num_claims=4)
        country_full_us = TotalCountryFactoryUS()
        country_full_cn = TotalCountryFactoryCN()
        appl_type = ApplTypeFactory(utility=True)
        language_en = LanguageFactory(english=True)
        language_cn = LanguageFactory(chinese=True)
        custom_details = CustomApplDetailsFactory(language=language_en)
        appl_details = ApplDetailsFactory(language=language_cn)
        family_option = FamOptionsFactory()
        desired_language = family_option.determine_desired_language(
            details=appl_details,
            country=country_full_cn,
            appl_type=appl_type,
            custom_details=custom_details)
        self.assertEquals(desired_language, language_en)

    def test_determine_desired_language_returns_default_no_custom_lang_provided(self):
        translated_details = ApplDetailsFactory(num_claims=4)
        country_full_us = TotalCountryFactoryUS()
        country_full_cn = TotalCountryFactoryCN()
        appl_type = ApplTypeFactory(utility=True)
        language_en = LanguageFactory(English=True)
        language_cn = LanguageFactory(Chinese=True)
        custom_details = CustomApplDetailsFactory(language=None)
        appl_details = ApplDetailsFactory(language=language_cn)
        family_option = FamOptionsFactory()
        desired_language = family_option.determine_desired_language(
            details=appl_details,
            country=country_full_cn,
            appl_type=appl_type,
            custom_details=custom_details)
        self.assertEquals(desired_language, language_cn)

    def test_determine_desired_language_returns_same_language_when_available(self):
        translated_details = ApplDetailsFactory(num_claims=4)
        # country_full_us = TotalCountryFactoryUS()
        # country_full_cn = TotalCountryFactoryCN()
        appl_type = ApplTypeFactory(utility=True)
        language_en = LanguageFactory(English=True)
        language_cn = LanguageFactory(Chinese=True)
        country_cn = CountryFactory(CN=True)
        AvailableLanguagesFactory(language=language_en,
                                  appl_type=appl_type,
                                  country=country_cn,
                                  default=False)
        AvailableLanguagesFactory(language=language_cn,
                                  appl_type=appl_type,
                                  country=country_cn,
                                  default=True)
        custom_details = CustomApplDetailsFactory(language=None)
        appl_details = ApplDetailsFactory(language=language_en)
        family_option = FamOptionsFactory()
        desired_language = family_option.determine_desired_language(
            details=appl_details,
            country=country_cn,
            appl_type=appl_type,
            custom_details=custom_details)
        self.assertEquals(desired_language, language_en)

    def test_determine_translation_full_required_same_language_as_default(self):
        appl_type = ApplTypeFactory(utility=True)
        language_en = LanguageFactory(English=True)
        language_cn = LanguageFactory(Chinese=True)
        # country_full_cn = TotalCountryFactoryCN()
        country_cn = CountryFactory(CN=True)
        AvailableLanguagesFactory(language=language_en,
                                  appl_type=appl_type,
                                  country=country_cn,
                                  default=True)
        AvailableLanguagesFactory(language=language_cn,
                                  appl_type=appl_type,
                                  country=country_cn,
                                  default=False)
        family_option = FamOptionsFactory()
        translation_enum = family_option.determine_extent_of_translation_required(
            old_language=language_en,
            new_language=language_cn,
            country=country_cn,
            appl_type=appl_type)
        self.assertEquals(TranslationRequirements.FULL_TRANSLATION, translation_enum)

    def test_determine_translation_full_required_same_old_language_same_as_new(self):
        appl_type = ApplTypeFactory(utility=True)
        language_en = LanguageFactory(English=True)
        language_cn = LanguageFactory(Chinese=True)
        # country_full_cn = TotalCountryFactoryCN()
        country_cn = CountryFactory(CN=True)
        AvailableLanguagesFactory(language=language_en,
                                  appl_type=appl_type,
                                  country=country_cn,
                                  default=True)
        AvailableLanguagesFactory(language=language_cn,
                                  appl_type=appl_type,
                                  country=country_cn,
                                  default=False)
        family_option = FamOptionsFactory()
        translation_enum = family_option.determine_extent_of_translation_required(
            old_language=language_cn,
            new_language=language_cn,
            country=country_cn,
            appl_type=appl_type)
        self.assertEquals(TranslationRequirements.NO_TRANSLATION, translation_enum)

    def test_determine_translation_required_ep_validation_official_language_old_lang(self):
        appl_type = ApplTypeFactory(epvalidation=True)
        language_en = LanguageFactory(English=True)
        language_de = LanguageFactory(German=True)
        # country_full_cn = TotalCountryFactoryCN()
        country_gb = CountryFactory(GB=True)
        AvailableLanguagesFactory(language=language_en,
                                  appl_type=appl_type,
                                  country=country_gb,
                                  default=True)
        family_option = FamOptionsFactory()
        translation_enum = family_option.determine_extent_of_translation_required(
            old_language=language_de,
            new_language=language_en,
            country=country_gb,
            appl_type=appl_type)
        self.assertEquals(TranslationRequirements.NO_TRANSLATION, translation_enum)

    def test_determine_translation_required_ep_validation_not_official_language_old_lang(self):
        appl_type = ApplTypeFactory(epvalidation=True)
        language_cn = LanguageFactory(Chinese=True)
        language_en = LanguageFactory(English=True)
        # country_full_cn = TotalCountryFactoryCN()
        country_gb = CountryFactory(GB=True)
        AvailableLanguagesFactory(language=language_en,
                                  appl_type=appl_type,
                                  country=country_gb,
                                  default=True)
        family_option = FamOptionsFactory()
        translation_enum = family_option.determine_extent_of_translation_required(
            old_language=language_cn,
            new_language=language_en,
            country=country_gb,
            appl_type=appl_type)
        self.assertEquals(TranslationRequirements.FULL_TRANSLATION, translation_enum)


class PCTApplOptionsTest(TestCase):

    def test_create_pct_appl_option_returns_appropriate_children_with_pct_appl_option(self):
        country = CountryFactory(US=True)
        appl_type = ApplTypeFactory(pct=True)
        oa_transform = OATransformFactory(country=country, appl_type=appl_type)
        date_filing = datetime(2020, 6, 4)
        language_cn = LanguageFactory(Chinese=True)
        dfltPublTrans = DefaultPublTransformFactory(appl_type=appl_type)
        dfltReqExamTrans = DefaultRequestExaminationTransformFactory(appl_type=appl_type)
        dfltOATrans = DefaultOATransformFactory(appl_type=appl_type)
        dfltAllowTrans = DefaultAllowanceTransformFactory(appl_type=appl_type)
        dfltIssueTrans = DefaultIssueTransformFactory(appl_type=appl_type)
        details = ApplDetailsFactory(language=language_cn)
        prev_appl_option = None
        oa_total = 2
        TranslationImplementedPseudoEnumFactory(no_translation=True)
        TranslationImplementedPseudoEnumFactory(full_translation=True)
        translation_enum = TranslationRequirements.NO_TRANSLATION
        fam_option = FamOptionsFactory()
        particulars = ApplOptionsParticularsFactory()
        appl_option = PCTApplOptions.objects.create_pct_appl_option(
            date_filing=date_filing, country=country,
            details=details,
            oa_total=2, fam_option=fam_option,
            isa_country=country,
            particulars=particulars, translation_enum=translation_enum,
            prev_appl_option=prev_appl_option)
        self.assertTrue(hasattr(appl_option, 'publoptions'))
        self.assertTrue(hasattr(appl_option, 'requestexaminationoptions'))
        self.assertEquals(appl_option.oaoptions_set.count(), 2)
        self.assertFalse(hasattr(appl_option, 'allowoptions'))
        self.assertFalse(hasattr(appl_option, 'issueoptions'))


class ApplOptionsTest(TestCase):

    def test_create_appl_option_prov_returns_appl_option_no_publ_etc(self):
        country = CountryFactory(US=True)
        appl_type = ApplTypeFactory(prov=True)
        oa_transform = OATransformFactory(country=country, appl_type=appl_type)
        date_filing = datetime(2020, 6, 4)
        language_cn = LanguageFactory(Chinese=True)
        dfltPublTrans = DefaultPublTransformFactory(appl_type=appl_type)
        dfltReqExamTrans = DefaultRequestExaminationTransformFactory(appl_type=appl_type)
        dfltOATrans = DefaultOATransformFactory(appl_type=appl_type)
        dfltAllowTrans = DefaultAllowanceTransformFactory(appl_type=appl_type)
        dfltIssueTrans = DefaultIssueTransformFactory(appl_type=appl_type)
        details = ApplDetailsFactory(language=language_cn)
        prev_appl_option = None
        oa_total = 2
        TranslationImplementedPseudoEnumFactory(no_translation=True)
        TranslationImplementedPseudoEnumFactory(full_translation=True)
        translation_enum = TranslationRequirements.NO_TRANSLATION
        fam_option = FamOptionsFactory()
        particulars = ApplOptionsParticularsFactory()
        appl_option = ApplOptions.objects.create_appl_option(
            date_filing=date_filing, country=country,
            appl_type=appl_type, details=details,
            oa_total=2, fam_option=fam_option,
            particulars=particulars, translation_enum=translation_enum,
            prev_appl_option=prev_appl_option)
        self.assertFalse(hasattr(appl_option, 'publoptions'))
        self.assertFalse(hasattr(appl_option, 'requestexaminationoptions'))
        self.assertEquals(appl_option.oaoptions_set.count(), 0)
        self.assertFalse(hasattr(appl_option, 'allowoptions'))
        self.assertFalse(hasattr(appl_option, 'issueoptions'))

    def test_create_appl_option_utility_returns_full_created_child_attr(self):
        country = CountryFactory(US=True)
        appl_type = ApplTypeFactory(utility=True)
        oa_transform = OATransformFactory(country=country, appl_type=appl_type)
        date_filing = datetime(2020, 6, 4)
        language_cn = LanguageFactory(Chinese=True)
        dfltPublTrans = DefaultPublTransformFactory(appl_type=appl_type)
        dfltReqExamTrans = DefaultRequestExaminationTransformFactory(appl_type=appl_type)
        dfltOATrans = DefaultOATransformFactory(appl_type=appl_type)
        dfltAllowTrans = DefaultAllowanceTransformFactory(appl_type=appl_type)
        dfltIssueTrans = DefaultIssueTransformFactory(appl_type=appl_type)
        details = ApplDetailsFactory(language=language_cn)
        prev_appl_option = None
        oa_total = 2
        TranslationImplementedPseudoEnumFactory(no_translation=True)
        TranslationImplementedPseudoEnumFactory(full_translation=True)
        translation_enum = TranslationRequirements.NO_TRANSLATION
        fam_option = FamOptionsFactory()
        particulars = ApplOptionsParticularsFactory()
        appl_option = ApplOptions.objects.create_appl_option(
            date_filing=date_filing, country=country,
            appl_type=appl_type, details=details,
            oa_total=2, fam_option=fam_option,
            particulars=particulars, translation_enum=translation_enum,
            prev_appl_option=prev_appl_option)
        self.assertTrue(hasattr(appl_option, 'publoptions'))
        self.assertTrue(hasattr(appl_option, 'requestexaminationoptions'))
        self.assertEquals(appl_option.oaoptions_set.count(), 2)
        self.assertTrue(hasattr(appl_option, 'allowoptions'))
        self.assertTrue(hasattr(appl_option, 'issueoptions'))

    def test_create_appl_option_ep_returns_appropriate_attr(self):
        country = CountryFactory(GB=True)
        appl_type = ApplTypeFactory(ep=True)
        oa_transform = OATransformFactory(country=country, appl_type=appl_type)
        date_filing = datetime(2020, 6, 4)
        language_cn = LanguageFactory(Chinese=True)
        dfltPublTrans = DefaultPublTransformFactory(appl_type=appl_type)
        dfltReqExamTrans = DefaultRequestExaminationTransformFactory(appl_type=appl_type)
        dfltOATrans = DefaultOATransformFactory(appl_type=appl_type)
        dfltAllowTrans = DefaultAllowanceTransformFactory(appl_type=appl_type)
        dfltIssueTrans = DefaultIssueTransformFactory(appl_type=appl_type)
        details = ApplDetailsFactory(language=language_cn)
        prev_appl_option = None
        oa_total = 2
        TranslationImplementedPseudoEnumFactory(no_translation=True)
        TranslationImplementedPseudoEnumFactory(full_translation=True)
        translation_enum = TranslationRequirements.NO_TRANSLATION
        fam_option = FamOptionsFactory()
        particulars = ApplOptionsParticularsFactory()
        appl_option = ApplOptions.objects.create_appl_option(
            date_filing=date_filing, country=country,
            appl_type=appl_type, details=details,
            oa_total=2, fam_option=fam_option,
            particulars=particulars, translation_enum=translation_enum,
            prev_appl_option=prev_appl_option)
        self.assertTrue(hasattr(appl_option, 'publoptions'))
        self.assertTrue(hasattr(appl_option, 'requestexaminationoptions'))
        self.assertEquals(appl_option.oaoptions_set.count(), 2)
        self.assertTrue(hasattr(appl_option, 'allowoptions'))
        self.assertFalse(hasattr(appl_option, 'issueoptions'))

    def test_create_appl_option_epvalid_returns_appropriate_attr(self):
        country = CountryFactory(GB=True)
        appl_type = ApplTypeFactory(epvalidation=True)
        oa_transform = OATransformFactory(country=country, appl_type=appl_type)
        date_filing = datetime(2020, 6, 4)
        language_cn = LanguageFactory(Chinese=True)
        dfltPublTrans = DefaultPublTransformFactory(appl_type=appl_type)
        dfltReqExamTrans = DefaultRequestExaminationTransformFactory(appl_type=appl_type)
        dfltOATrans = DefaultOATransformFactory(appl_type=appl_type)
        dfltAllowTrans = DefaultAllowanceTransformFactory(appl_type=appl_type)
        dfltIssueTrans = DefaultIssueTransformFactory(appl_type=appl_type)
        details = ApplDetailsFactory(language=language_cn)
        prev_appl_option = None
        oa_total = 2
        TranslationImplementedPseudoEnumFactory(no_translation=True)
        TranslationImplementedPseudoEnumFactory(full_translation=True)
        translation_enum = TranslationRequirements.NO_TRANSLATION
        fam_option = FamOptionsFactory()
        particulars = ApplOptionsParticularsFactory()
        appl_option = ApplOptions.objects.create_appl_option(
            date_filing=date_filing, country=country,
            appl_type=appl_type, details=details,
            oa_total=2, fam_option=fam_option,
            particulars=particulars, translation_enum=translation_enum,
            prev_appl_option=prev_appl_option)
        self.assertFalse(hasattr(appl_option, 'publoptions'))
        self.assertFalse(hasattr(appl_option, 'requestexaminationoptions'))
        self.assertEquals(appl_option.oaoptions_set.count(), 0)
        self.assertFalse(hasattr(appl_option, 'allowoptions'))
        self.assertTrue(hasattr(appl_option, 'issueoptions'))

    def test_create_appl_option_pctnatphase_returns_exception(self):
        country = CountryFactory(GB=True)
        appl_type = ApplTypeFactory(nationalphase=True)
        oa_transform = OATransformFactory(country=country, appl_type=appl_type)
        date_filing = datetime(2020, 6, 4)
        language_cn = LanguageFactory(Chinese=True)
        dfltPublTrans = DefaultPublTransformFactory(appl_type=appl_type)
        dfltReqExamTrans = DefaultRequestExaminationTransformFactory(appl_type=appl_type)
        dfltOATrans = DefaultOATransformFactory(appl_type=appl_type)
        dfltAllowTrans = DefaultAllowanceTransformFactory(appl_type=appl_type)
        dfltIssueTrans = DefaultIssueTransformFactory(appl_type=appl_type)
        details = ApplDetailsFactory(language=language_cn)
        prev_appl_option = None
        oa_total = 2
        TranslationImplementedPseudoEnumFactory(no_translation=True)
        TranslationImplementedPseudoEnumFactory(full_translation=True)
        translation_enum = TranslationRequirements.NO_TRANSLATION
        fam_option = FamOptionsFactory()
        particulars = ApplOptionsParticularsFactory()
        self.assertRaises(ApplTypePCTNationalPhaseNotSupportedException,
                          ApplOptions.objects.create_appl_option,
                          date_filing=date_filing, country=country,
                          appl_type=appl_type, details=details,
                          oa_total=2, fam_option=fam_option,
                          particulars=particulars, translation_enum=translation_enum,
                          prev_appl_option=prev_appl_option)

    def test_create_appl_option_pct_returns_not_supported_exception(self):
        country = CountryFactory(GB=True)
        appl_type = ApplTypeFactory(pct=True)
        oa_transform = OATransformFactory(country=country, appl_type=appl_type)
        date_filing = datetime(2020, 6, 4)
        language_cn = LanguageFactory(Chinese=True)
        dfltPublTrans = DefaultPublTransformFactory(appl_type=appl_type)
        dfltReqExamTrans = DefaultRequestExaminationTransformFactory(appl_type=appl_type)
        dfltOATrans = DefaultOATransformFactory(appl_type=appl_type)
        dfltAllowTrans = DefaultAllowanceTransformFactory(appl_type=appl_type)
        dfltIssueTrans = DefaultIssueTransformFactory(appl_type=appl_type)
        details = ApplDetailsFactory(language=language_cn)
        prev_appl_option = None
        oa_total = 2
        TranslationImplementedPseudoEnumFactory(no_translation=True)
        TranslationImplementedPseudoEnumFactory(full_translation=True)
        translation_enum = TranslationRequirements.NO_TRANSLATION
        fam_option = FamOptionsFactory()
        particulars = ApplOptionsParticularsFactory()
        self.assertRaises(ApplTypePCTNotSupportedException,
                          ApplOptions.objects.create_appl_option,
                          date_filing=date_filing, country=country,
                          appl_type=appl_type, details=details,
                          oa_total=2, fam_option=fam_option,
                          particulars=particulars, translation_enum=translation_enum,
                          prev_appl_option=prev_appl_option)

    def test_create_examination_creates_request_and_all_two_oa_options(self):
        country = CountryFactory(CN=True)
        appl_type_utility = ApplTypeFactory(utility=True)
        request_examination_transform_utility = RequestExaminationTransformFactory(country=country,
                                                                                   appl_type=appl_type_utility)
        oa_transform_utility = OATransformFactory(country=country, appl_type=appl_type_utility)
        appl_option = ApplOptionsFactory(country=country, appl_type=appl_type_utility)
        appl_option.create_examination(oa_total=2)
        self.assertEquals(OAOptions.objects.all().count(), 2)
        self.assertEquals(RequestExaminationOptions.objects.all().count(), 1)


class PublOptionsTest(TestCase):

    def test_create_publ_option_creates_publOption(self):
        country = CountryFactory(CN=True)
        appl_option = ApplOptionsFactory(country=country)
        publ_trans = DefaultPublTransformFactory()
        publ_option = PublOptions.objects.create_option(appl_option=appl_option)
        self.assertEquals(publ_option, PublOptions.objects.first())

    def test_create_publ_option_returns_publ_option(self):
        country = CountryFactory(CN=True)
        appl_option = ApplOptionsFactory(country=country)
        publ_transform = PublicationTransformFactory(country=country)
        publ_option = PublOptions.objects.create_option(appl_option=appl_option)
        self.assertEquals(publ_option.date_diff, publ_transform.date_diff)

    def test_create_publ_option_returns_publ_option_two_options(self):
        country = CountryFactory(CN=True)
        country_us = CountryFactory(US=True)
        appl_option = ApplOptionsFactory(country=country)
        publ_transform = PublicationTransformFactory(country=country)
        publ_transform_us = PublicationTransformFactory(country=country_us)
        publ_option = PublOptions.objects.create_option(appl_option=appl_option)
        self.assertEquals(publ_option.date_diff, publ_transform.date_diff)

    def test_create_publ_option_returns_publ_option_not_default_option(self):
        country = CountryFactory(CN=True)
        appl_option = ApplOptionsFactory(country=country)
        publ_trans = DefaultPublTransformFactory()
        publ_transform = PublicationTransformFactory(country=country)
        publ_option = PublOptions.objects.create_option(appl_option=appl_option)
        self.assertEquals(publ_option.date_diff, publ_transform.date_diff)

    def test_create_publ_option_returns_default_option_not_wrong_country_version(self):
        country = CountryFactory(CN=True)
        country_us = CountryFactory(US=True)
        appl_option = ApplOptionsFactory(country=country)
        publ_trans = DefaultPublTransformFactory()
        publ_transform = PublicationTransformFactory(country=country_us)
        publ_option = PublOptions.objects.create_option(appl_option=appl_option)
        self.assertEquals(publ_option.date_diff, publ_trans.date_diff)

    def test_publ_transform_uses_correct_appl_type(self):
        appl_type_utility = ApplTypeFactory(utility=True)
        appl_type_pct = ApplTypeFactory(pct=True)
        country = CountryFactory(CN=True)
        publ_transform_utility = PublicationTransformFactory(country=country, appl_type=appl_type_utility)
        publ_transform_pct = PublicationTransformFactory(country=country, appl_type=appl_type_pct)
        appl_option_pct = ApplOptionsFactory(country=country, appl_type=appl_type_pct)
        publ_option = PublOptions.objects.create_option(appl_option=appl_option_pct)
        # publ_option = appl_option_pct.create_publ_option()
        self.assertEquals(publ_option.date_diff, publ_transform_pct.date_diff)


class RequestExaminationOptionsTest(TestCase):
    # ***********************************
    # create_request_examination
    # ***********************************

    def test_create_request_examination_option_creates_request_examinationOption(self):
        country = CountryFactory(CN=True)
        appl_option = ApplOptionsFactory(country=country)
        request_examination_trans = DefaultRequestExaminationTransformFactory()
        request_examination_option = RequestExaminationOptions.objects.create_option(appl_option=appl_option)
        self.assertEquals(request_examination_option, RequestExaminationOptions.objects.first())

    def test_create_request_examination_option_returns_request_examination_option(self):
        country = CountryFactory(CN=True)
        appl_option = ApplOptionsFactory(country=country)
        request_examination_transform = RequestExaminationTransformFactory(country=country)
        request_examination_option = RequestExaminationOptions.objects.create_option(appl_option=appl_option)
        self.assertEquals(request_examination_option.date_diff, request_examination_transform.date_diff)

    def test_create_request_examination_option_returns_request_examination_option_two_options(self):
        country = CountryFactory(CN=True)
        country_us = CountryFactory(US=True)
        appl_option = ApplOptionsFactory(country=country)
        request_examination_transform = RequestExaminationTransformFactory(country=country)
        request_examination_transform_us = RequestExaminationTransformFactory(country=country_us)
        request_examination_option = RequestExaminationOptions.objects.create_option(appl_option=appl_option)
        self.assertEquals(request_examination_option.date_diff, request_examination_transform.date_diff)

    def test_create_request_examination_option_returns_request_examination_option_not_default_option(self):
        country = CountryFactory(CN=True)
        appl_option = ApplOptionsFactory(country=country)
        request_examination_trans = DefaultRequestExaminationTransformFactory()
        request_examination_transform = RequestExaminationTransformFactory(country=country)
        request_examination_option = RequestExaminationOptions.objects.create_option(appl_option=appl_option)
        self.assertEquals(request_examination_option.date_diff, request_examination_transform.date_diff)

    def test_create_request_examination_option_returns_default_option_not_wrong_country_version(self):
        country = CountryFactory(CN=True)
        country_us = CountryFactory(US=True)
        appl_option = ApplOptionsFactory(country=country)
        request_examination_trans = DefaultRequestExaminationTransformFactory()
        request_examination_transform = RequestExaminationTransformFactory(country=country_us)
        request_examination_option = RequestExaminationOptions.objects.create_option(appl_option=appl_option)
        self.assertEquals(request_examination_option.date_diff, request_examination_trans.date_diff)

    def test_request_examination_transform_uses_correct_appl_type(self):
        appl_type_utility = ApplTypeFactory(utility=True)
        appl_type_pct = ApplTypeFactory(pct=True)
        country = CountryFactory(CN=True)
        request_examination_transform_utility = RequestExaminationTransformFactory(country=country,
                                                                                   appl_type=appl_type_utility)
        request_examination_transform_pct = RequestExaminationTransformFactory(country=country, appl_type=appl_type_pct)
        appl_option_pct = ApplOptionsFactory(country=country, appl_type=appl_type_pct)
        request_examination_option = RequestExaminationOptions.objects.create_option(appl_option=appl_option_pct)
        self.assertEquals(request_examination_option.date_diff, request_examination_transform_pct.date_diff)


class AllowanceOptionsTest(TestCase):
    # ***********************************
    # create_allow
    # ***********************************

    def test_create_allow_option_creates_allowOption(self):
        country = CountryFactory(CN=True)
        appl_option = ApplOptionsFactory(country=country)
        allow_trans = DefaultAllowanceTransformFactory()
        allow_option = AllowOptions.objects.create_option(appl_option=appl_option)
        self.assertEquals(allow_option, AllowOptions.objects.first())

    def test_create_allow_option_returns_allow_option(self):
        country = CountryFactory(CN=True)
        appl_option = ApplOptionsFactory(country=country)
        allow_transform = AllowanceTransformFactory(country=country)
        allow_option = AllowOptions.objects.create_option(appl_option=appl_option)
        self.assertEquals(allow_option.date_diff, allow_transform.date_diff)

    def test_create_allow_option_returns_allow_option_two_options(self):
        country = CountryFactory(CN=True)
        country_us = CountryFactory(US=True)
        appl_option = ApplOptionsFactory(country=country)
        allow_transform = AllowanceTransformFactory(country=country)
        allow_transform_us = AllowanceTransformFactory(country=country_us)
        allow_option = AllowOptions.objects.create_option(appl_option=appl_option)
        self.assertEquals(allow_option.date_diff, allow_transform.date_diff)

    def test_create_allow_option_returns_allow_option_not_default_option(self):
        country = CountryFactory(CN=True)
        appl_option = ApplOptionsFactory(country=country)
        allow_trans = DefaultAllowanceTransformFactory()
        allow_transform = AllowanceTransformFactory(country=country)
        allow_option = AllowOptions.objects.create_option(appl_option=appl_option)
        self.assertEquals(allow_option.date_diff, allow_transform.date_diff)

    def test_create_allow_option_returns_default_option_not_wrong_country_version(self):
        country = CountryFactory(CN=True)
        country_us = CountryFactory(US=True)
        appl_option = ApplOptionsFactory(country=country)
        allow_trans = DefaultAllowanceTransformFactory()
        allow_transform = AllowanceTransformFactory(country=country_us)
        allow_option = AllowOptions.objects.create_option(appl_option=appl_option)
        self.assertEquals(allow_option.date_diff, allow_trans.date_diff)

    def test_allow_transform_uses_correct_appl_type(self):
        appl_type_utility = ApplTypeFactory(utility=True)
        appl_type_pct = ApplTypeFactory(pct=True)
        country = CountryFactory(CN=True)
        allow_transform_utility = AllowanceTransformFactory(country=country, appl_type=appl_type_utility)
        allow_transform_pct = AllowanceTransformFactory(country=country, appl_type=appl_type_pct)
        appl_option_pct = ApplOptionsFactory(country=country, appl_type=appl_type_pct)
        allow_option = AllowOptions.objects.create_option(appl_option=appl_option_pct)
        self.assertEquals(allow_option.date_diff, allow_transform_pct.date_diff)


class IssueOptionsTest(TestCase):
    # ***********************************
    # create_issue
    # ***********************************

    def test_create_issue_option_creates_issueOption(self):
        country = CountryFactory(CN=True)
        appl_option = ApplOptionsFactory(country=country)
        issue_trans = DefaultIssueTransformFactory()
        issue_option = IssueOptions.objects.create_option(appl_option=appl_option)
        self.assertEquals(issue_option, IssueOptions.objects.first())

    def test_create_option_returns_issue_option(self):
        country = CountryFactory(CN=True)
        appl_option = ApplOptionsFactory(country=country)
        issue_transform = IssueTransformFactory(country=country)
        issue_option = IssueOptions.objects.create_option(appl_option=appl_option)
        self.assertEquals(issue_option.date_diff, issue_transform.date_diff)

    def test_create_option_returns_issue_option_two_options(self):
        country = CountryFactory(CN=True)
        country_us = CountryFactory(US=True)
        appl_option = ApplOptionsFactory(country=country)
        issue_transform = IssueTransformFactory(country=country)
        issue_transform_us = IssueTransformFactory(country=country_us)
        issue_option = IssueOptions.objects.create_option(appl_option=appl_option)
        self.assertEquals(issue_option.date_diff, issue_transform.date_diff)

    def test_create_option_returns_issue_option_not_default_option(self):
        country = CountryFactory(CN=True)
        appl_option = ApplOptionsFactory(country=country)
        issue_trans = DefaultIssueTransformFactory()
        issue_transform = IssueTransformFactory(country=country)
        issue_option = IssueOptions.objects.create_option(appl_option=appl_option)
        self.assertEquals(issue_option.date_diff, issue_transform.date_diff)

    def test_create_option_returns_default_option_not_wrong_country_version(self):
        country = CountryFactory(CN=True)
        country_us = CountryFactory(US=True)
        appl_option = ApplOptionsFactory(country=country)
        issue_trans = DefaultIssueTransformFactory()
        issue_transform = IssueTransformFactory(country=country_us)
        issue_option = IssueOptions.objects.create_option(appl_option=appl_option)
        self.assertEquals(issue_option.date_diff, issue_trans.date_diff)

    def test_issue_transform_uses_correct_appl_type(self):
        appl_type_utility = ApplTypeFactory(utility=True)
        appl_type_pct = ApplTypeFactory(pct=True)
        country = CountryFactory(CN=True)
        issue_transform_utility = IssueTransformFactory(country=country, appl_type=appl_type_utility)
        issue_transform_pct = IssueTransformFactory(country=country, appl_type=appl_type_pct)
        appl_option_pct = ApplOptionsFactory(country=country, appl_type=appl_type_pct)
        issue_option = IssueOptions.objects.create_option(appl_option=appl_option_pct)
        self.assertEquals(issue_option.date_diff, issue_transform_pct.date_diff)


class OAOptionsTest(TestCase):
    def test_create_all_oa_options_creates_three_and_connects(self):
        country = CountryFactory(CN=True)
        appl_type_utility = ApplTypeFactory(utility=True)
        oa_transform_utility = OATransformFactory(country=country, appl_type=appl_type_utility)
        appl_option = ApplOptionsFactory(country=country, appl_type=appl_type_utility)
        oa_array = OAOptions.objects.create_all_oa_options(appl_option=appl_option, oa_total=3)
        self.assertEquals(len(oa_array), 3)
        self.assertEquals(oa_array[0], oa_array[1].oa_prev)
        self.assertEquals(oa_array[1], oa_array[2].oa_prev)

        # ***********************************
        # create_oa
        # ***********************************

    def test_create_oa_option_creates_oaOption(self):
        country = CountryFactory(CN=True)
        appl_option = ApplOptionsFactory(country=country)
        oa_trans = DefaultOATransformFactory()
        oa_option = OAOptions.objects.create_option(appl_option=appl_option, oa_prev=None)
        self.assertEquals(oa_option, OAOptions.objects.first())

    def test_create_oa_option_returns_oa_option(self):
        country = CountryFactory(CN=True)
        appl_option = ApplOptionsFactory(country=country)
        oa_transform = OATransformFactory(country=country)
        oa_option = OAOptions.objects.create_option(appl_option=appl_option, oa_prev=None)
        self.assertEquals(oa_option.date_diff, oa_transform.date_diff)

    def test_create_oa_option_returns_oa_option_two_options(self):
        country = CountryFactory(CN=True)
        country_us = CountryFactory(US=True)
        appl_option = ApplOptionsFactory(country=country)
        oa_transform = OATransformFactory(country=country)
        oa_transform_us = OATransformFactory(country=country_us)
        oa_option = OAOptions.objects.create_option(appl_option=appl_option, oa_prev=None)
        self.assertEquals(oa_option.date_diff, oa_transform.date_diff)

    def test_create_oa_option_returns_oa_option_not_default_option(self):
        country = CountryFactory(CN=True)
        appl_option = ApplOptionsFactory(country=country)
        oa_trans = DefaultOATransformFactory()
        oa_transform = OATransformFactory(country=country)
        oa_option = OAOptions.objects.create_option(appl_option=appl_option, oa_prev=None)
        self.assertEquals(oa_option.date_diff, oa_transform.date_diff)

    def test_create_oa_option_returns_default_option_not_wrong_country_version(self):
        country = CountryFactory(CN=True)
        country_us = CountryFactory(US=True)
        appl_option = ApplOptionsFactory(country=country)
        oa_trans = DefaultOATransformFactory()
        oa_transform = OATransformFactory(country=country_us)
        oa_option = OAOptions.objects.create_option(appl_option=appl_option, oa_prev=None)
        self.assertEquals(oa_option.date_diff, oa_trans.date_diff)

    def test_oa_transform_uses_correct_appl_type(self):
        appl_type_utility = ApplTypeFactory(utility=True)
        appl_type_pct = ApplTypeFactory(pct=True)
        country = CountryFactory(CN=True)
        oa_transform_utility = OATransformFactory(country=country, appl_type=appl_type_utility)
        oa_transform_pct = OATransformFactory(country=country, appl_type=appl_type_pct)
        appl_option_pct = ApplOptionsFactory(country=country, appl_type=appl_type_pct)
        oa_option = OAOptions.objects.create_option(appl_option=appl_option_pct, oa_prev=None)
        self.assertEquals(oa_option.date_diff, oa_transform_pct.date_diff)

    def test_oa_transforms_with_previous(self):
        country = CountryFactory(CN=True)
        appl_type_utility = ApplTypeFactory(utility=True)
        oa_prev = OAOptionsFactory()
        oa_transform_utility = OATransformFactory(country=country, appl_type=appl_type_utility)
        appl_option = ApplOptionsFactory(country=country, appl_type=appl_type_utility)
        oa_option = OAOptions.objects.create_option(appl_option=appl_option, oa_prev=oa_prev)
        self.assertEquals(oa_option.oa_prev, oa_prev)

    def test_create_all_oa_options_creates_one(self):
        country = CountryFactory(CN=True)
        appl_type_utility = ApplTypeFactory(utility=True)
        oa_transform_utility = OATransformFactory(country=country, appl_type=appl_type_utility)
        appl_option = ApplOptionsFactory(country=country, appl_type=appl_type_utility)
        oa_array = appl_option.create_all_oa_options(oa_total=1)
        self.assertEquals(len(oa_array), 1)
        self.assertIsInstance(oa_array[0], OAOptions)
