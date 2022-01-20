from application.models.baseApplication import BaseApplication

from application.models.publication import Publication
from application.models.requestExamination import RequestExamination
from application.models.allowance import Allowance
from application.models.issue import Issue
from application.models.officeAction import OfficeAction


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

        oas_out = self._generate_oa(date_request_examination=req.date_request_examination, oas_in=oas_in)
        # calc last oa
        last_date = self.date_filing
        for oa in oas_out:
            if oa.date_office_action > last_date:
                last_date = oa.date_office_action

        allow_date_diff = options.allowoptions.date_diff
        # generate allowance date and estimates
        allowance = self._generate_allowance(allow_date_diff, last_date)
        issue_date_diff = options.issueoptions.date_diff
        # generate issue date and estimates
        self._generate_issue(issue_date_diff, allowance.date_allowance)

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

    def _create_ordered_oa(self, oas_in):
        ordered_oa = []
        oa_first = [x for x in oas_in if x.oa_prev is None]
        ordered_oa.append(oa_first[0])
        prev_oa = oa_first[0]
        # order array

        complete = False
        while complete is False:
            oa_x = [x for x in oas_in if x.oa_prev_id == prev_oa.id]
            if len(oa_x) != 0:
                prev_oa = oa_x[0]
                ordered_oa.append(oa_x[0])
            else:
                complete = True

        return ordered_oa

    def _generate_oa(self, date_request_examination, oas_in):
        ordered_oa = self._create_ordered_oa(oas_in=oas_in)

        # date_prev = self.date_filing
        date_prev = date_request_examination
        oa_array = []
        prev_oa = None
        for oa in ordered_oa:
            date_oa = date_prev + oa.date_diff
            created_oa = OfficeAction.objects.create(application=self,
                                                     oa_prev=prev_oa,
                                                     date_office_action=date_oa)
            created_oa.generate_ests()
            oa_array.append(created_oa)
            date_prev = date_oa
            prev_oa = created_oa

        return oa_array

    def _generate_allowance(self, date_allow_diff, date_last_oa):
        date_allowance = date_allow_diff + date_last_oa

        allow = Allowance.objects.create(
            application=self,
            date_allowance=date_allowance)
        allow.generate_ests()
        return allow

    def _generate_issue(self, date_diff, date_allowance):
        date_issuance = date_diff + date_allowance
        issue = Issue.objects.create(
            application=self,
            date_issuance=date_issuance,
        )
        issue.generate_ests()
        return issue

