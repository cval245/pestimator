from django.db import models

from application.models.baseApplication import BaseApplication
from application.models.officeAction import OfficeAction
from application.models.publication import Publication
from application.models.requestExamination import RequestExamination
from application.utils import convert_class_applType
from characteristics.models import Country, EntitySize
from estimation import utils
from estimation.models import FilingEstimate, FilingEstimateTemplate, LawFirmEst


class PCTApplication(BaseApplication):
    # normal country variable is the REceiveing office
    # isa_country is the International Search Authority Country
    isa_country = models.ForeignKey(Country, on_delete=models.CASCADE)
    isa_entity_size = models.ForeignKey(EntitySize, on_delete=models.CASCADE, null=True)

    class Meta:
        abstract = False
        # Todo possibly add meta options constraint to ensure isa_country
        # is valid for country.  maybe not due to db compatibility issues

    def _generate_filing_est(self):
        # calculates costs for PCT in RO country (country)
        # excluding ISA ONLY costs and then calculates ISA oNly costs in ISA country
        self._generate_translation_est()

        filing_templates = FilingEstimateTemplate.objects.filter(
            country=self.country,
            appl_type=convert_class_applType(self),
        )
        templates = utils.filter_conditions(filing_templates, self)
        # filter for NOT ISA country
        templates = templates.filter(conditions__isa_country_fee_only=False)
        templates = templates.select_related('law_firm_template')
        ests = []
        for e in templates:
            lawFirmEst = None
            if e.law_firm_template is not None:
                lawFirmEst = LawFirmEst.objects.create(
                    date=e.law_firm_template.date_diff + self.date_filing,
                    law_firm_cost=e.law_firm_template.law_firm_cost
                )

            est = FilingEstimate.objects.create_complex_and_simple_est(
                application=self,
                law_firm_est=lawFirmEst,
                est_template=e,
            )
            ests.append(est)

        # filter for ISA country
        filing_templates = FilingEstimateTemplate.objects.filter(
            country=self.isa_country,
            appl_type=convert_class_applType(self),
        )
        templates = filing_templates.filter(conditions__isa_country_fee_only=True)
        templates = utils.filter_conditions(templates, self, isa_filter=True)
        # do same thing,
        templates = templates.select_related('law_firm_template')
        for e in templates:
            lawFirmEst = None
            if e.law_firm_template is not None:
                lawFirmEst = LawFirmEst.objects.create(
                    date=e.law_firm_template.date_diff + self.date_filing,
                    law_firm_cost=e.law_firm_template.law_firm_cost
                )

            est = FilingEstimate.objects.create_complex_and_simple_est(
                application=self,
                law_firm_est=lawFirmEst,
                est_template=e,
            )
            ests.append(est)

        return ests

    def generate_dates(self, options):
        # generate filing estimates

        # generate publication date and estimates
        publ = self._generate_publication(options.publoptions.date_diff)

        self._generate_filing_est()
        publ.generate_ests()

    def _generate_publication(self, publication_diff_from_filing):
        # lookup the publication time_diff
        publ = Publication.objects.create(
            application=self,
            date_publication=self.date_filing + publication_diff_from_filing)
        return publ
        # create a publication instance
