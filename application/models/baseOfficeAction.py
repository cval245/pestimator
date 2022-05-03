from django.db import models

from application.utils import convert_class_applType
from estimation import utils
from estimation.models import LawFirmEst, OAEstimate, OAEstimateTemplate


class BaseOfficeAction(models.Model):
    date_office_action = models.DateField()
    application = models.ForeignKey(
        'BaseUtilityApplication', on_delete=models.CASCADE, related_name='officeaction_set'
    )
    oa_prev = models.ForeignKey('self', models.SET_NULL, null=True)

    class Meta:
        abstract = True

    def generate_ests(self):

        oa_templates = OAEstimateTemplate.objects.basic_template_filter(
            country=self.application.country,
            appl_type=convert_class_applType(self.application),
            date=self.date_office_action,
        )
        templates = utils.filter_conditions(oa_templates, self.application)
        templates = templates.select_related('law_firm_template')
        ests = []
        for e in templates:
            lawFirmEst = None
            if e.law_firm_template is not None:
                lawFirmEst = LawFirmEst.objects.create(
                    date=e.law_firm_template.date_diff + self.date_office_action,
                    law_firm_cost=e.law_firm_template.law_firm_cost
                )

            est = OAEstimate.objects.create_complex_and_simple_est(
                application=self.application,
                law_firm_est=lawFirmEst,
                office_action=self,
                est_template=e,
            )
            ests.append(est)

        return ests
