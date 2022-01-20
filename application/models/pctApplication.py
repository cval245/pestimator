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
        self._generate_filing_est()

        # generate publication date and estimates
        publ = self._generate_publication(options.publoptions.date_diff)
        # TODO
        # req = self._generate_request_examination(options.requestexaminationoptions.date_diff)
        #
        # if req:
        #     oas_in = options.oaoptions_set.all()
        #     oas_out = self._generate_oa(date_request_examination=req.date_request_examination, args=oas_in)
        # calc last oa

    def _generate_publication(self, publication_diff_from_filing):
        # lookup the publication time_diff
        publ = Publication.objects.create(
            application=self,
            date_publication=self.date_filing + publication_diff_from_filing)
        publ.generate_ests()
        return publ
        # create a publication instance

    def _generate_request_examination(self, date_diff_from_filing):
        req = RequestExamination.objects.create(
            application=self,
            date_request_examination=self.date_filing + date_diff_from_filing
        )
        req.generate_ests()
        return req

    def _generate_oa(self, date_request_examination, args):
        ordered_oa = []
        oa_first = [x for x in args if x.oa_prev is None]
        ordered_oa.append(oa_first[0])
        prev_oa = oa_first[0]
        # order array
        complete = False
        while complete is False:
            oa_x = [x for x in args if x.oa_prev == prev_oa]
            if len(oa_x) != 0:
                prev_oa = oa_x[0]
                ordered_oa.append(oa_x[0])
            else:
                complete = True

        date_prev = date_request_examination  # self.date_filing
        oa_array = []
        for oa in ordered_oa:
            date_oa = date_prev + oa.date_diff
            created_oa = OfficeAction.objects.create(application=self,
                                                     date_office_action=date_oa)
            created_oa.generate_ests()
            oa_array.append(created_oa)
            date_prev = date_oa

        return oa_array
