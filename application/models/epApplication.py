from application.models import BaseUtilityApplication


class EPApplication(BaseUtilityApplication):
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
        # generate issue date and estimates

    def _generate_request_examination(self, date_diff_from_filing):
        from application.models.requestExamination import RequestExamination
        req = RequestExamination.objects.create(
            application=self,
            date_request_examination=self.date_filing + date_diff_from_filing
        )
        req.generate_ests()
        return req
