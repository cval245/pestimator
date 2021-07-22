from django.db import models

from application.models.baseApplication import BaseApplication
from application.utils import convert_class_applType
from estimation import utils


class Publication(models.Model):
    date_publication = models.DateField()
    application = models.OneToOneField(
        BaseApplication, on_delete=models.CASCADE,
    )

    class Meta:
        abstract = False

    def generate_ests(self):
        from estimation.models import PublicationEstTemplate
        publ_templates = PublicationEstTemplate.objects.filter(
            country=self.application.country,
            appl_type=convert_class_applType(self.application)
        )
        templates = utils.filter_conditions(publ_templates, self.application.details)\
            .select_related('law_firm_template')

        ests = []
        for e in templates:
            lawFirmEst = None
            if e.law_firm_template is not None:
                from estimation.models import LawFirmEst
                lawFirmEst = LawFirmEst.objects.create(
                    date=e.law_firm_template.date_diff + self.date_publication,
                    law_firm_cost=e.law_firm_template.law_firm_cost
                )

            from estimation.models import PublicationEst
            est = PublicationEst.objects.create(
                publication=self,
                date=e.date_diff + self.date_publication,
                official_cost=e.official_cost,
                law_firm_est=lawFirmEst,
                application=self.application
            )
            ests.append(est)

        return ests
