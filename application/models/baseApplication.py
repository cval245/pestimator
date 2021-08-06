from django.conf import settings
from django.db import models

from application import utils as applUtils
from application.models import ApplDetails
from application.models.managers import ApplManager
from application.utils import convert_class_applType
from characteristics.models import Country
from estimation import utils
from famform.models import ApplOptions
from family.models import Family


class BaseApplication(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    title = models.TextField()
    family = models.ForeignKey(Family, on_delete=models.CASCADE)
    date_filing = models.DateField()
    details = models.OneToOneField(ApplDetails, on_delete=models.CASCADE)
    prior_appl = models.ForeignKey("self", models.SET_NULL, null=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    appl_option = models.OneToOneField(ApplOptions, on_delete=models.CASCADE)

    objects = ApplManager()

    class Meta:
        abstract = False

    def get_appl_type(self):
        return applUtils.convert_class_applType(self)

    def generate_dates(self, options):
        # generate filing estimates
        self._generate_filing_est()

        # generate publication date and estimates
        self._generate_publication(options.publoptions.date_diff)
        # calc last oa
        last_date = self.date_filing

    def _generate_publication(self, publication_diff_from_filing):
        from application.models.publication import Publication
        publ = Publication.objects.create(
            application=self,
            date_publication=self.date_filing + publication_diff_from_filing)
        publ.generate_ests()
        return publ
        # create a publication instance


    def _generate_filing_est(self):

        from estimation.models import FilingEstimateTemplate
        filing_templates = FilingEstimateTemplate.objects.filter(
            country=self.country,
            appl_type=convert_class_applType(self)
        )
        templates = utils.filter_conditions(filing_templates, self.details)

        templates = templates.select_related('law_firm_template')
        print('\n\nself.country', self.country)
        print('templates = ', templates)
        ests = []
        for e in templates:
            lawFirmEst = None
            print('e.law_ = ', e.law_firm_template)
            if e.law_firm_template is not None:
                from estimation.models import LawFirmEst
                lawFirmEst = LawFirmEst.objects.create(
                    date=e.law_firm_template.date_diff + self.date_filing,
                    law_firm_cost=e.law_firm_template.law_firm_cost
                )

            from estimation.models import FilingEstimate
            est = FilingEstimate.objects.create(
                application=self,
                date=e.date_diff + self.date_filing,
                official_cost=e.official_cost,
                law_firm_est=lawFirmEst,
            )
            ests.append(est)

        return ests