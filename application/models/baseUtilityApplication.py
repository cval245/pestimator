from application.models.baseApplication import BaseApplication


class BaseUtilityApplication(BaseApplication):

    class Meta:
        abstract = False



    def generate_dates(self, options):
        # generate filing estimates
        self._generate_filing_est()

        # generate publication date and estimates
        publ = self._generate_publication(options.publoptions.date_diff)
        req = self._generate_request_examination(options.requestexaminationoptions.date_diff)

        oas_in = options.oaoptions_set.all()

        oas_out = self._generate_oa(date_request_examination=req.date_request_examination, args=oas_in)
        # calc last oa
        last_date = self.date_filing
        for oa in oas_out:
            if (oa.date_office_action > last_date):
                last_date = oa.date_office_action

        allow_date_diff = options.allowoptions.date_diff
        # generate allowance date and estimates
        allowance = self._generate_allowance(allow_date_diff, last_date)
        issue_date_diff = options.issueoptions.date_diff
        # generate issue date and estimates
        self._generate_issue(issue_date_diff, allowance.date_allowance)

    def _generate_publication(self, publication_diff_from_filing):
        # lookup the publication time_diff
        from application.models.publication import Publication
        publ = Publication.objects.create(
            application=self,
            date_publication=self.date_filing + publication_diff_from_filing)
        publ.generate_ests()
        return publ
        # create a publication instance

    def _generate_request_examination(self, date_diff_from_filing):
        from application.models.requestExamination import RequestExamination
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

        date_prev = self.date_filing
        oa_array = []
        for oa in ordered_oa:
            date_oa = date_prev + oa.date_diff
            from application.models.officeAction import OfficeAction
            created_oa = OfficeAction.objects.create(application=self,
                                                     date_office_action=date_oa)
            created_oa.generate_ests()
            oa_array.append(created_oa)
            date_prev = date_oa

        return oa_array

    def _generate_allowance(self, date_allow_diff, date_last_oa):
        date_allowance = date_allow_diff + date_last_oa
        from application.models.allowance import Allowance
        allow = Allowance.objects.create(
            application=self.baseutilityapplication,
            date_allowance=date_allowance)
        allow.generate_ests()
        return allow

    def _generate_issue(self, date_diff, date_allowance):
        date_issuance = date_diff + date_allowance
        from application.models.issue import Issue
        issue = Issue.objects.create(
            application=self.baseutilityapplication,
            date_issuance=date_issuance,
        )
        issue.generate_ests()
        return issue

    # def _generate_filing_est(self):
    #
    #     from estimation.models import FilingEstimateTemplate
    #     filing_templates = FilingEstimateTemplate.objects.filter(
    #         country=self.country,
    #         appl_type=convert_class_applType(self)
    #     )
    #     templates = utils.filter_conditions(filing_templates, self.details)
    #     from estimation.models import FilingEstimate
    #     ests = [
    #         FilingEstimate.objects.create(
    #             application=self,
    #             date=e.date_diff + self.date_filing,
    #             official_cost=e.official_cost
    #         )
    #         for e in templates
    #     ]
    #     return ests
