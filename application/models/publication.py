from django.db import models

from application.utils import convert_class_applType
from estimation import utils
from estimation.models import LawFirmEst, PublicationEst, PublicationEstTemplate


class Publication(models.Model):
    date_publication = models.DateField()
    application = models.OneToOneField(
        'BaseApplication', on_delete=models.CASCADE,
    )

    class Meta:
        abstract = False

    def generate_ests(self):

        publ_templates = PublicationEstTemplate.objects.basic_template_filter(
            country=self.application.country,
            appl_type=convert_class_applType(self.application),
            date=self.date_publication,
        )
        templates = utils.filter_conditions(publ_templates, self.application) \
            .select_related('law_firm_template')

        ests = []
        for e in templates:
            lawFirmEst = None
            if e.law_firm_template is not None:
                lawFirmEst = LawFirmEst.objects.create(
                    date=e.law_firm_template.date_diff + self.date_publication,
                    law_firm_cost=e.law_firm_template.law_firm_cost
                )

            est = PublicationEst.objects.create_complex_and_simple_est(
                application=self.application,
                law_firm_est=lawFirmEst,
                publication=self,
                est_template=e,
            )
            ests.append(est)

        return ests
