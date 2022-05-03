from django.db import models

from application.models import BaseOfficeAction
from application.utils import convert_class_applType
from estimation import utils
from estimation.models import LawFirmEst, USOAEstimate, USOAEstimateTemplate


class USOfficeAction(BaseOfficeAction):
    oa_final_bool = models.BooleanField(default=False)
    # override foreign key
    application = models.ForeignKey(
        'USUtilityApplication', on_delete=models.CASCADE,
    )

    class Meta:
        abstract = False

    def generate_ests(self):

        foas = USOfficeAction.objects.filter(application=self.application, oa_final_bool=True)
        if foas.count() == 1:
            oa_first_final_bool = True
        else:
            oa_first_final_bool = False

        oa_templates = USOAEstimateTemplate.objects.basic_template_filter(
            country=self.application.country,
            appl_type=convert_class_applType(self.application),
            date=self.date_office_action,
            oa_final_bool=self.oa_final_bool,
            oa_first_final_bool=oa_first_final_bool,
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

            est = USOAEstimate.objects.create_complex_and_simple_est(
                application=self.application,
                law_firm_est=lawFirmEst,
                office_action=self,
                est_template=e,
            )
            ests.append(est)

        return ests