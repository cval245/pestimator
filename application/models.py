from django.conf import settings
from django.db import models
from datetime import date
from dateutil.relativedelta import relativedelta
from estimation import utils
from characteristics.models import EntitySize, ApplType
from family.models import Family

class ApplManager(models.Manager):

    def create_full(self, options, user, family_id):
        self.create_correct_appl(options, user, family_id)
        

    def generate_appl(self, options, user, family_id):
        applDetails = options.details
        applDetails.pk = None
        applDetails.save()
        appl = self.create(user=user, title=options.title,
                           date_filing=options.date_filing,
                           family_id=family_id,
                           details=applDetails)
        appl.generate_dates(options)
        return appl


    def create_correct_appl(self, options, user, family_id):

        if (options.appl_type.application_type == 'prov'):
            # create prov
            ProvApplication.objects.generate_appl(options=options, user=user, family_id=family_id)
        elif (options.appl_type.application_type == 'pct'):
            # create pct
            PCTApplication.objects.generate_appl(options=options, user=user, family_id=family_id)
        elif (options.appl_type.application_type == 'utility'):
            # create utility
            if options.country.country == 'US':
                # US Utility Application
                USUtilityApplication.objects.generate_appl(options=options,user=user, family_id=family_id)
            else:
                # Generic Utility Application
                UtilityApplication.objects.generate_appl(options=options, user=user, family_id=family_id)

    
class ApplDetails(models.Model):
    num_indep_claims = models.IntegerField()
    num_pages = models.IntegerField()
    num_claims = models.IntegerField()
    num_drawings = models.IntegerField()
    entity_size = models.ForeignKey(EntitySize, on_delete=models.CASCADE)


class BaseApplication(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    title = models.TextField()
    family = models.ForeignKey(Family, on_delete=models.CASCADE)
    date_filing = models.DateField()
    details = models.OneToOneField(ApplDetails, on_delete=models.CASCADE)
    prior_appl = models.ForeignKey("self", models.SET_NULL, null=True)

    objects = ApplManager()

    class Meta:
        abstract = False

    # def select_ests(self):
    #     # select filing ests
    #     filing_est = self.filingestimate_set.all()\
    #         .values('application_id','official_cost', 'date', 'law_firm_est')
    #     publ_est = self.publication.publicationest_set.all()\
    #         .values('publication_id','official_cost', 'date', 'law_firm_est')

    #     total_est = filing_est.union(publ_est)
    #     return total_est


    def generate_dates(self, options):
        # generate filing estimates
        self._generate_filing_est()

        # generate publication date and estimates
        self._generate_publication(options.publoptions.date_diff)
        # calc last oa
        last_date = self.date_filing

    def _generate_publication(self, publication_diff_from_filing):
        # lookup the publication time_diff
        publ = Publication.objects.create(
            application=self,
            date_publication=self.date_filing + publication_diff_from_filing)
        publ.generate_ests()
        return publ
        # create a publication instance


    def _generate_filing_est(self):

        from estimation.models import FilingEstimateTemplate, FilingEstimate,\
            LawFirmEst
        filing_templates = FilingEstimateTemplate.objects.all()
        templates = utils.filter_conditions(filing_templates, self.details)

        templates = templates.select_related('law_firm_template')
        ests = []
        for e in templates:
            lawFirmEst = None
            if e.law_firm_template is not None:
                lawFirmEst = LawFirmEst.objects.create(
                    date=e.law_firm_template.date_diff+self.date_filing,
                    law_firm_cost=e.law_firm_template.law_firm_cost
                )

            est = FilingEstimate.objects.create(
                application=self,
                date=e.date_diff + self.date_filing,
                official_cost=e.official_cost,
                law_firm_est=lawFirmEst,
            )
            ests.append(est)

        return ests

class ProvApplication(BaseApplication):

    class Meta:
        abstract = False


class PCTApplication(BaseApplication):

    class Meta:
        abstract = False

class EPApplication(BaseApplication):


    # def select_ests(self):
    #     # select filing ests
    #     filing_est = self.filingestimate_set.all()\
    #         .values('application_id','official_cost', 'date', 'law_firm_est')
    #     publ_est = self.publication.publicationest_set.all()\
    #         .values('publication_id','official_cost', 'date', 'law_firm_est')
    #     oa_est = OAEstimate.objects.filter(office_action__application=self.id)\
    #         .values('officeaction_id','official_cost', 'date', 'law_firm_est')
    #     allow_est = self.allowance.allowancest_set.all()\
    #         .values('allowance_id','official_cost', 'date', 'law_firm_est')

    #     total_est = filing_est.union(publ_est, oa_est, allow_est)
    #     return total_est


    class Meta:
        abstract = False


class BaseUtilityApplication(BaseApplication):

    class Meta:
        abstract = False


    # def select_ests(self):
    #     # select filing ests
    #     filing_est = self.filingestimate_set.all()\
    #         .values('application_id','official_cost', 'date', 'law_firm_est')
    #     publ_est = self.publication.publicationest_set.all()\
    #         .values('publication_id','official_cost', 'date', 'law_firm_est')
    #     oa_est = OAEstimate.objects.filter(office_action__application=self.id)\
    #         .values('officeaction_id','official_cost', 'date', 'law_firm_est')
    #     allow_est = self.allowance.allowancest_set.all()\
    #         .values('allowance_id','official_cost', 'date', 'law_firm_est')
    #     issue_est = self.issue.issueest_set.all()\
    #         .values('issue_id','official_cost', 'date', 'law_firm_est')

    #     total_est = filing_est.union(publ_est, oa_est, allow_est, issue_est)
    #     return total_est



    def generate_dates(self, options):
        # generate filing estimates
        self._generate_filing_est()

        # generate publication date and estimates
        self._generate_publication(options.publoptions.date_diff)
        oas_in = options.oaoptions_set.all()

        oas_out = self._generate_oa(oas_in)

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
        publ = Publication.objects.create(
            application=self,
            date_publication=self.date_filing + publication_diff_from_filing)
        publ.generate_ests()
        return publ
        # create a publication instance

    def _generate_oa(self, args):
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
            created_oa = OfficeAction.objects.create(application=self,
                                                     date_office_action=date_oa)
            created_oa.generate_ests()
            oa_array.append(created_oa)
            date_prev = date_oa

        return oa_array

    def _generate_allowance(self, date_allow_diff, date_last_oa):
        date_allowance = date_allow_diff + date_last_oa
        allow = Allowance.objects.create(
            application=self.baseutilityapplication,
            date_allowance=date_allowance)
        allow.generate_ests()
        return allow

    def _generate_issue(self, date_diff, date_allowance):
        date_issuance = date_diff + date_allowance
        issue = Issue.objects.create(
            application=self.baseutilityapplication,
            date_issuance=date_issuance,
        )
        issue.generate_ests()
        return issue


    def _generate_filing_est(self):

        from estimation.models import FilingEstimateTemplate, FilingEstimate
        filing_templates = FilingEstimateTemplate.objects.all()
        templates = utils.filter_conditions(filing_templates, self.details)
        ests = [
            FilingEstimate.objects.create(
                application=self,
                date=e.date_diff + self.date_filing,
                official_cost=e.official_cost
            )
            for e in templates
        ]
        return ests


class UtilityApplication(BaseUtilityApplication):

    class Meta:
        abstract = False


class USUtilityApplication(BaseUtilityApplication):

    class Meta:
        abstract = False


    # def select_ests(self):
    #     from estimation.models import USOAEstimate
    #     # select filing ests
    #     filing_est = self.filingestimate_set.all()\
    #         .values('application_id','official_cost', 'date', 'law_firm_est')
    #     publ_est = self.publication.publicationest_set.all()\
    #         .values('publication_id','official_cost', 'date', 'law_firm_est')
    #     oa_est = USOAEstimate.objects.filter(office_action__application=self.id)\
    #         .values('usofficeaction','official_cost', 'date', 'law_firm_est')
    #     allow_est = self.allowance.allowanceest_set.all()\
    #         .values('allowance_id','official_cost', 'date', 'law_firm_est')
    #     issue_est = self.issue.issueest_set.all()\
    #         .values('issue_id','official_cost', 'date', 'law_firm_est')

    #     total_est = filing_est.union(publ_est, oa_est, allow_est, issue_est)
    #     return total_est


    def _generate_oa(self, args):
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
        final_oa_bool = False
        for oa in ordered_oa:
            date_oa = date_prev + oa.date_diff
            created_oa = USOfficeAction.objects.create(
                application=self,
                oa_final_bool=final_oa_bool,
                date_office_action=date_oa)
            created_oa.generate_ests()
            oa_array.append(created_oa)
            date_prev = date_oa
            if final_oa_bool is False:
                final_oa_bool = True
            else:
                final_oa_bool = False

        return oa_array


class BaseOfficeAction(models.Model):
    date_office_action = models.DateField()
    application = models.ForeignKey(
        UtilityApplication, on_delete=models.CASCADE,
    )
    oa_prev = models.ForeignKey('self', models.SET_NULL, null=True)

    class Meta:
        abstract = True

    def generate_ests(self):
        from estimation.models import OAEstimateTemplate, OAEstimate
        oa_templates = OAEstimateTemplate.objects.all()
        templates = utils.filter_conditions(oa_templates, self.application.details)

        templates = templates.select_related('law_firm_template')
        ests = []
        for e in templates:
            lawFirmEst = None
            if e.law_firm_template is not None:
                lawFirmEst = LawFirmEst.objects.create(
                    date=e.law_firm_template.date_diff+self.date_filing,
                    law_firm_cost=e.law_firm_template.law_firm_cost
                )

            est = OAEstimate.objects.create(
                office_action=self,
                date=e.date_diff + self.date_office_action,
                official_cost=e.official_cost,
                law_firm_est=lawFirmEst,
                application=self.application               
            )
            ests.append(est)

        return ests

class OfficeAction(BaseOfficeAction):

    class Meta:
        abstract = False




class USOfficeAction(BaseOfficeAction):
    oa_final_bool = models.BooleanField(default=False)
    # override foreign key
    application = models.ForeignKey(
        USUtilityApplication, on_delete=models.CASCADE,
    )

    class Meta:
        abstract = False

    def generate_ests(self):
        from estimation.models import USOAEstimateTemplate, USOAEstimate
        oa_templates = USOAEstimateTemplate.objects.all()
        templates = utils.filter_conditions(oa_templates, self.application.details)

        templates = templates.select_related('law_firm_template')
        ests = []
        for e in templates:
            lawFirmEst = None
            if e.law_firm_template is not None:
                lawFirmEst = LawFirmEst.objects.create(
                    date=e.law_firm_template.date_diff+self.date_filing,
                    law_firm_cost=e.law_firm_template.law_firm_cost
                )

            est = USOAEstimate.objects.create(
                office_action=self,
                date=e.date_diff + self.date_office_action,
                official_cost=e.official_cost,
                law_firm_est=lawFirmEst,
                application=self.application                
            )
            ests.append(est)

        return ests



class Publication(models.Model):
    date_publication = models.DateField()
    application = models.OneToOneField(
        BaseApplication, on_delete=models.CASCADE,
    )

    class Meta:
        abstract = False

    def generate_ests(self):
        from estimation.models import PublicationEstTemplate, PublicationEst
        publ_templates = PublicationEstTemplate.objects.all()
        templates = utils.filter_conditions(publ_templates, self.application.details)

        templates = templates.select_related('law_firm_template')
        ests = []
        for e in templates:
            lawFirmEst = None
            if e.law_firm_template is not None:
                lawFirmEst = LawFirmEst.objects.create(
                    date=e.law_firm_template.date_diff+self.date_filing,
                    law_firm_cost=e.law_firm_template.law_firm_cost
                )

            est = PublicationEst.objects.create(
                publication=self,
                date=e.date_diff + self.date_publication,
                official_cost=e.official_cost,
                law_firm_est=lawFirmEst,
                application=self.application                
            )
            ests.append(est)


        return ests


class EPPublication(models.Model):
    date_publication = models.DateField()
    application = models.OneToOneField(
        EPApplication, on_delete=models.CASCADE,
    )

    class Meta:
        abstract = False



class BaseAllowance(models.Model):
    application = models.OneToOneField(
        BaseUtilityApplication, on_delete=models.CASCADE,
    )
    date_allowance = models.DateField()

    def generate_ests(self):
        from estimation.models import AllowanceEstTemplate, AllowanceEst
        allow_templates = AllowanceEstTemplate.objects.all()
        templates = utils.filter_conditions(allow_templates, self.application.details)
        templates = templates.select_related('law_firm_template')
        ests = []
        for e in templates:
            lawFirmEst = None
            if e.law_firm_template is not None:
                lawFirmEst = LawFirmEst.objects.create(
                    date=e.law_firm_template.date_diff+self.date_filing,
                    law_firm_cost=e.law_firm_template.law_firm_cost
                )

            est = AllowanceEst.objects.create(
                allowance=self,
                date=e.date_diff + self.date_allowance,
                official_cost=e.official_cost,
                law_firm_est=lawFirmEst,
                application=self.application
            )
            ests.append(est)

        return ests

    class Meta:
        abstract = True

class Allowance(BaseAllowance):

    class Meta:
        abstract = False

class BaseIssue(models.Model):
    application = models.OneToOneField(
        BaseUtilityApplication, on_delete=models.CASCADE,
    )
    date_issuance = models.DateField()

    class Meta:
        abstract = True

    def generate_ests(self):
        from estimation.models import IssueEstTemplate, IssueEst
        issue_templates = IssueEstTemplate.objects.all()
        templates = utils.filter_conditions(issue_templates, self.application.details)
        templates = templates.select_related('law_firm_template')
        ests = []
        for e in templates:
            lawFirmEst = None
            if e.law_firm_template is not None:
                lawFirmEst = LawFirmEst.objects.create(
                    date=e.law_firm_template.date_diff+self.date_filing,
                    law_firm_cost=e.law_firm_template.law_firm_cost
                )

            est = IssueEst.objects.create(
                issue=self,
                date=e.date_diff + self.date_issuance,
                official_cost=e.official_cost,
                law_firm_est=lawFirmEst,
                application=self.application
            )
            ests.append(est)

        return ests

class Issue(BaseIssue):

    class Meta:
        abstract = False


