from django.db import models

from application.models.baseUtilityApplication import BaseUtilityApplication
from application.utils import convert_class_applType
from estimation import utils

class BaseAllowance(models.Model):
    application = models.OneToOneField(
        BaseUtilityApplication, on_delete=models.CASCADE,
    )
    date_allowance = models.DateField()

    def generate_ests(self):

        from estimation.models import AllowanceEstTemplate
        allow_templates = AllowanceEstTemplate.objects.filter(
            country=self.application.country,
            appl_type=convert_class_applType(self.application)
        )
        templates = utils.filter_conditions(allow_templates, self.application.details)
        templates = templates.select_related('law_firm_template')
        ests = []
        for e in templates:
            lawFirmEst = None
            if e.law_firm_template is not None:
                from estimation.models import LawFirmEst
                lawFirmEst = LawFirmEst.objects.create(
                    date=e.law_firm_template.date_diff+self.date_allowance,
                    law_firm_cost=e.law_firm_template.law_firm_cost
                )
            from estimation.models import AllowanceEst
            est = AllowanceEst.objects.create(
                allowance=self,
                date=e.date_diff + self.date_allowance,
                official_cost=e.official_cost,
                law_firm_est=lawFirmEst,
                application=self.application
            )
            ests.append(est)

        return ests

    class Meta:
        abstract = True