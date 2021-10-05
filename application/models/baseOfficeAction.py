from django.db import models

from application.models import BaseUtilityApplication
from application.utils import convert_class_applType
from estimation import utils

class BaseOfficeAction(models.Model):
    date_office_action = models.DateField()
    application = models.ForeignKey(
        BaseUtilityApplication, on_delete=models.CASCADE,
    )
    oa_prev = models.ForeignKey('self', models.SET_NULL, null=True)

    class Meta:
        abstract = True

    def generate_ests(self):

        from estimation.models import OAEstimateTemplate
        oa_templates = OAEstimateTemplate.objects.filter(
            country=self.application.country,
            appl_type=convert_class_applType(self.application),
        )
        templates = utils.filter_conditions(oa_templates, self.application)
        templates = templates.select_related('law_firm_template')
        ests = []
        for e in templates:
            lawFirmEst = None
            if e.law_firm_template is not None:
                from estimation.models import LawFirmEst
                lawFirmEst = LawFirmEst.objects.create(
                    date=e.law_firm_template.date_diff + self.date_office_action,
                    law_firm_cost=e.law_firm_template.law_firm_cost
                )

            from estimation.models import OAEstimate
            est = OAEstimate.objects.create_complex_and_simple_est(
                application=self.application,
                law_firm_est=lawFirmEst,
                office_action=self,
                est_template=e,
            )
            # est = OAEstimate.objects.create(
            #     office_action=self,
            #     date=e.date_diff + self.date_office_action,
            #     official_cost=e.official_cost,
            #     law_firm_est=lawFirmEst,
            #     application=self.application
            # )
            ests.append(est)

        return ests