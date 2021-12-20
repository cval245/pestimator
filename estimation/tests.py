from django.test import TestCase
from . import factories

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
