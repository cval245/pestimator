from application.models.baseApplication import BaseApplication


class EPValidationApplication(BaseApplication):
    class Meta:
        abstract = False

    def generate_dates(self, options):
        # generate filing estimates
        self._generate_filing_est()

        # calc last oa
        last_date = self.date_filing

        # generate allowance date and estimates
        issue_date_diff = options.issueoptions.date_diff
        # generate issue date and estimates
        self._generate_issue(issue_date_diff, last_date)

    def _generate_issue(self, date_diff, date_allowance):
        date_issuance = date_diff + date_allowance
        from application.models.epValidationIssue import EPValidationIssue
        issue = EPValidationIssue.objects.create(
            application=self.epvalidationapplication,
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