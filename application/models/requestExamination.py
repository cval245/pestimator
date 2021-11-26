from django.db import models

from application.models.baseApplication import BaseApplication
from application.utils import convert_class_applType
from estimation import utils


class RequestExamination(models.Model):
    date_request_examination = models.DateField()
    application = models.OneToOneField(
        BaseApplication, on_delete=models.CASCADE,
    )

    class Meta:
        abstract = False

    def generate_ests(self):

        from estimation.models import RequestExamEstTemplate
        req_templates = RequestExamEstTemplate.objects.filter(
            country=self.application.country,
            appl_type=convert_class_applType(self.application),
        )
        templates = utils.filter_conditions(req_templates, self.application) \
            .select_related('law_firm_template')

        ests = []
        for e in templates:
            lawFirmEst = None
            if e.law_firm_template is not None:
                from estimation.models import LawFirmEst
                lawFirmEst = LawFirmEst.objects.create(
                    date=e.law_firm_template.date_diff + self.date_request_examination,
                    law_firm_cost=e.law_firm_template.law_firm_cost
                )

            from estimation.models import RequestExamEst
            est = RequestExamEst.objects.create_complex_and_simple_est(
                application=self.application,
                law_firm_est=lawFirmEst,
                exam_request=self,
                est_template=e,
            )
            ests.append(est)

        return ests
