from application.models import BaseUtilityApplication

from application.models.usOfficeAction import USOfficeAction
from famform.models.USOAOptions import USOAOptions


class USUtilityApplication(BaseUtilityApplication):
    class Meta:
        abstract = False

    def generate_dates(self, options):
        # generate filing estimates
        # self._generate_filing_est()

        # generate publication date and estimates
        publ = self._generate_publication(options.publoptions.date_diff)
        req = self._generate_request_examination(options.requestexaminationoptions.date_diff)

        oas_in = USOAOptions.objects.filter(appl=options).select_related()

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

    def _generate_oa(self, date_request_examination, oas_in):
        ordered_oa = self._create_ordered_oa(oas_in=oas_in)
        date_prev = date_request_examination
        oa_array = []
        prev_oa = None
        for oa in ordered_oa:
            date_oa = date_prev + oa.date_diff
            created_oa = USOfficeAction.objects.create(
                application=self,
                oa_final_bool=oa.oa_final_bool,
                oa_prev=prev_oa,
                date_office_action=date_oa)
            # created_oa.generate_ests()
            oa_array.append(created_oa)
            date_prev = date_oa
            prev_oa = created_oa

        return oa_array