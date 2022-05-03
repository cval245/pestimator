from django.db import models

from application.utils import convert_class_applType
from estimation import utils
from estimation.models import AllowanceEst, AllowanceEstTemplate, LawFirmEst


class BaseAllowance(models.Model):
    application = models.OneToOneField(
        "application.BaseUtilityApplication", on_delete=models.CASCADE, null=True,
        related_name='allowance'

    )
    date_allowance = models.DateField()

    def generate_ests(self):

        allow_templates = AllowanceEstTemplate.objects.basic_template_filter(
            country=self.application.country,
            appl_type=convert_class_applType(self.application),
            date=self.date_allowance,
        )
        templates = utils.filter_conditions(allow_templates, self.application)
        templates = templates.select_related('law_firm_template')
        ests = []
        for e in templates:
            lawFirmEst = None
            if e.law_firm_template is not None:
                lawFirmEst = LawFirmEst.objects.create(
                    date=e.law_firm_template.date_diff + self.date_allowance,
                    law_firm_cost=e.law_firm_template.law_firm_cost
                )

            est = AllowanceEst.objects.create_complex_and_simple_est(
                application=self.application,
                law_firm_est=lawFirmEst,
                allowance=self,
                est_template=e,
            )

            ests.append(est)
        return ests

    class Meta:
        abstract = True