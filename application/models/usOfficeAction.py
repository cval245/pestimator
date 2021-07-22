from django.db import models

from application.models import BaseOfficeAction, USUtilityApplication
from application.utils import convert_class_applType
from estimation import utils

class USOfficeAction(BaseOfficeAction):
    oa_final_bool = models.BooleanField(default=False)
    # override foreign key
    application = models.ForeignKey(
        USUtilityApplication, on_delete=models.CASCADE,
    )

    class Meta:
        abstract = False

    def generate_ests(self):

        #from estimation.models import Law
        from estimation.models import USOAEstimateTemplate
        oa_templates = USOAEstimateTemplate.objects.filter(
            country=self.application.country,
            appl_type=convert_class_applType(self.application)
        )
        templates = utils.filter_conditions(oa_templates, self.application.details)

        templates = templates.select_related('law_firm_template')
        ests = []
        for e in templates:
            lawFirmEst = None
            if e.law_firm_template is not None:
                from estimation.models import LawFirmEst
                lawFirmEst = LawFirmEst.objects.create(
                    date=e.law_firm_template.date_diff+self.date_office_action,
                    law_firm_cost=e.law_firm_template.law_firm_cost
                )

            from estimation.models import USOAEstimate
            est = USOAEstimate.objects.create(
                office_action=self,
                date=e.date_diff + self.date_office_action,
                official_cost=e.official_cost,
                law_firm_est=lawFirmEst,
                application=self.application
            )
            ests.append(est)

        return ests