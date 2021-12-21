from datetime import date

from django.test import TestCase

from application.factories import AllowanceFactory, ApplDetailsFactory, BaseUtilityApplicationFactory, IssuanceFactory, \
    OfficeActionFactory, PCTApplicationFactory, PublicationFactory, RequestExaminationFactory
from application.models import RequestExamination
from characteristics.factories import ApplTypeFactory, CountryFactory, DocFormatFactory, EntitySizeFactory, \
    LanguageFactory
from famform.factories import AllowOptionsFactory, ApplOptionsFactory, ApplOptionsParticularsFactory, \
    IssueOptionsFactory, OAOptionsFactory, \
    PublOptionFactory, RequestExaminationOptionFactory
from . import factories
from . import utils
from .models import FilingEstimateTemplate


class TestLawFirmEst(TestCase):

    def test_func(self):
        lawfirmEst = factories.LawFirmEstFactory()
        self.lineTemp = factories.LineEstimationTemplateConditionsFactory()
        self.LawFirmEstTemp = factories.LawFirmEstTemplateFactory()
        self.filing = factories.FilingEstimateTemplateFactory()
        self.publ = factories.PublicationEstTemplateFactory()
        self.oa = factories.OAEstimateTemplateFactory()
        self.usoa = factories.USOAEstimateTemplateFactory()
        self.allow = factories.AllowanceEstTemplateFactory()
        self.issue = factories.IssueEstTemplateFactory()
        self.transEstTemp = factories.TranslationEstTemplateFactory()
        self.dfltTransEstTemp = factories.DefaultTranslationEstTemplateFactory()

        self.BaseEst = factories.BaseEstFactory()
        self.FilEst = factories.FilingEstimateFactory()
        self.oaEst = factories.OAEstimateFactory()
        self.usoaEst = factories.USOAEstimateFactory()
        self.publEst = factories.PublicationEstFactory()
        self.allowEst = factories.AllowanceEstFactory()
        self.issueEst = factories.IssueEstFactory()

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
        filtered = utils._filter_entity_size(templates=templates, appl_details=appl_details)
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
        filtered = utils._filter_entity_size(templates=templates, appl_details=appl_details)
        self.assertEquals(filtered.count(), 1)
        self.assertEquals(filtered.first(), filing_est_template)
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
