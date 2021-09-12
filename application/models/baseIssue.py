from django.db import models

from application.models import BaseUtilityApplication
from application.utils import convert_class_applType
from estimation import utils

class BaseIssue(models.Model):
    application = models.OneToOneField(
        BaseUtilityApplication, on_delete=models.CASCADE,
    )
    date_issuance = models.DateField()

    class Meta:
        abstract = True


    def generate_ests(self):

        from estimation.models import IssueEstTemplate
        issue_templates = IssueEstTemplate.objects.filter(
            country=self.application.country,
            appl_type=convert_class_applType(self.application),
        )
        templates = utils.filter_conditions(issue_templates, self.application)
        templates = templates.select_related('law_firm_template')
        ests = []
        for e in templates:
            lawFirmEst = None
            if e.law_firm_template is not None:
                from estimation.models import LawFirmEst
                lawFirmEst = LawFirmEst.objects.create(
                    date=e.law_firm_template.date_diff + self.date_issuance,
                    law_firm_cost=e.law_firm_template.law_firm_cost
                )

            from estimation.models import IssueEst
            est = IssueEst.objects.create_complex_and_simple_est(
                application=self.application,
                law_firm_est=lawFirmEst,
                issuance=self,
                est_template=e,
            )
            ests.append(est)
        return ests