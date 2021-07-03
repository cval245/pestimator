from django.test import TestCase
from datetime import date
from djmoney.money import Money
from .models import UtilityApplication, Publication, Allowance, OfficeAction, Issue, ApplDetails
from django.contrib.auth import get_user_model
from dateutil.relativedelta import relativedelta
from django.db.models import Sum
from characteristics.models import EntitySize, Country, ApplType
from estimation.models import LineEstimationTemplateConditions, FilingEstimateTemplate,\
    OAEstimate, OAEstimateTemplate,\
    PublicationEstTemplate, AllowanceEstTemplate, IssueEstTemplate,\
    PublicationEst, AllowanceEst, IssueEst
from famform.models import FamOptions, ApplOptions, AllowOptions, PublOptions,\
    OAOptions, IssueOptions
from family.models import Family

# Create your tests here.
class UtilityApplicationTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(username='test',
                                                         password='Belgrade2010',
                                                         email='c.val@tutanota.com')
        self.entitySize = EntitySize.objects.create(entity_size='test')
        self.family = Family.objects.create(user=self.user,
                                            family_name='title of family',
                                            family_no='no of family')
        self.applDetails = ApplDetails.objects.create(
            num_indep_claims=1,
            num_pages=10,
            num_claims=10,
            num_drawings=5,
            entity_size=self.entitySize)
        self.filing_date = date(2020, 1, 1)
        self.country = Country.objects.create(country='US',currency_name= 'USD')
        self.applType = ApplType.objects.create(application_type='test')
        self.options = FamOptions.objects.create(
            family=self.family
        )
        self.applOption = ApplOptions.objects.create(details=self.applDetails,
                                                     country=self.country,
                                                     appl_type=self.applType,
                                                     date_filing=date(2020,1,1),
                                                     title='title',
                                                     fam_options=self.options,
                                                     prev_appl_options=None
        )
        self.publOption = PublOptions.objects.create(appl=self.applOption,
                                                     date_diff=relativedelta(years=1))
        self.oAOption = OAOptions.objects.create(appl=self.applOption,
                                                 date_diff=relativedelta(years=1),
                                                 oa_prev=None)
        self.oAOption_two = OAOptions.objects.create(appl=self.applOption,
                                                     date_diff=relativedelta(years=1),
                                                     oa_prev=self.oAOption)
        self.oAOption_three = OAOptions.objects.create(appl=self.applOption,
                                                       date_diff=relativedelta(years=1),
                                                       oa_prev=self.oAOption_two)


        self.allowOption = AllowOptions.objects.create(appl=self.applOption,
                                                       date_diff=relativedelta(years=1))
        self.issueOption = IssueOptions.objects.create(appl=self.applOption,
                                                       date_diff=relativedelta(years=1))

        self.utilityApplDetails = ApplDetails.objects.create(
            num_indep_claims=1,
            num_pages=1,
            num_claims=1,
            num_drawings=1,
            entity_size=self.entitySize,
        )
        self.utilityApplication = UtilityApplication.objects.create(
            user=self.user, title='title',
            date_filing=date(2020, 1, 1),
            details=self.utilityApplDetails
        )
        self.conditions = LineEstimationTemplateConditions.objects.create(
            condition_claims_min=0,
            #condition_claims_max=Null,
            condition_drawings_min=0,
            #condition_drawings_max=0,
            condition_pages_min=0,
            #condition_pages_max=0,
            condition_entity_size=self.entitySize,
        )
        self.filing_template = FilingEstimateTemplate.objects.create(
            date_diff=relativedelta(years=1),
            official_cost=Money(1, 'USD'),
            country=self.country,
            conditions=self.conditions,
        )
        self.publication_template = PublicationEstTemplate.objects.create(
            date_diff=relativedelta(years=1),
            official_cost=Money(2, 'USD'),
            country=self.country,
            conditions=self.conditions,
        )
        self.oa_template = OAEstimateTemplate.objects.create(
            date_diff=relativedelta(years=1),
            official_cost=Money(3, 'USD'),
            country=self.country,
            conditions=self.conditions,
        )
        self.allowance_template = AllowanceEstTemplate.objects.create(
            date_diff=relativedelta(years=1),
            official_cost=Money(4, 'USD'),
            country=self.country,
            conditions=self.conditions,
        )
        self.issue_template = IssueEstTemplate.objects.create(
            date_diff=relativedelta(years=1),
            official_cost=Money(5, 'USD'),
            country=self.country,
            conditions=self.conditions,
        )

    def test_create_full_creates_Publication(self):
        selectedApplOption = ApplOptions.objects.get(id=self.applOption.id)
        UtilityApplication.objects.create_full(options=selectedApplOption, user=self.user)
        date_publication = self.filing_date + relativedelta(years=1)
        self.assertEquals(date_publication, Publication.objects.first().date_publication)

    def test_create_full_creates_oa(self):
        selectedApplOption = ApplOptions.objects.get(id=self.applOption.id)
        UtilityApplication.objects.create_full(options=selectedApplOption, user=self.user)
        # relativedelta is calced by combining options in Setup
        date_allowance = self.filing_date + relativedelta(years=1)
        self.assertEquals(date_allowance, OfficeAction.objects.first().date_office_action)

    def test_create_full_creates_allowance(self):
        selectedApplOption = ApplOptions.objects.get(id=self.applOption.id)
        UtilityApplication.objects.create_full(options=selectedApplOption, user=self.user)
        # relativedelta is calced by combining options in Setup
        oa_agg = selectedApplOption.oaoptions_set.all().aggregate(date_diff=Sum('date_diff'))
        allow_diff = selectedApplOption.allowoptions.date_diff
        date_allowance = self.filing_date + oa_agg['date_diff'] + allow_diff
        self.assertEquals(date_allowance, Allowance.objects.first().date_allowance)

    def test_create_full_creates_issue(self):
        selectedApplOption = ApplOptions.objects.get(id=self.applOption.id)
        UtilityApplication.objects.create_full(options=selectedApplOption,
                                               user=self.user)
        oa_agg = selectedApplOption.oaoptions_set.all().aggregate(date_diff=Sum('date_diff'))
        allow_diff = selectedApplOption.allowoptions.date_diff
        issue_diff = selectedApplOption.issueoptions.date_diff
        date_issuance = self.filing_date + oa_agg['date_diff'] + allow_diff + issue_diff
        self.assertEquals(date_issuance, Issue.objects.first().date_issuance)

    def test_generate_filing_est(self):
        ests = self.utilityApplication._generate_filing_est()
        self.assertEquals(ests[0].official_cost, self.filing_template.official_cost)

    def test_create_full_publication_est(self):
        selectedApplOption = ApplOptions.objects.get(id=self.applOption.id)
        UtilityApplication.objects.create_full(options=selectedApplOption, user=self.user)
        self.assertEquals(self.publication_template.official_cost,
                          PublicationEst.objects.all().first().official_cost
        )

    def test_create_full_oa_est(self):
        selectedApplOption = ApplOptions.objects.get(id=self.applOption.id)
        UtilityApplication.objects.create_full(options=selectedApplOption, user=self.user)
        self.assertEquals(self.oa_template.official_cost,
                          OAEstimate.objects.all().first().official_cost
        )

    def test_create_full_allowance_est(self):
        selectedApplOption = ApplOptions.objects.select_related().get(id=self.applOption.id)
        UtilityApplication.objects.create_full(options=selectedApplOption, user=self.user)
        self.assertEquals(self.allowance_template.official_cost,
                          AllowanceEst.objects.all().first().official_cost
        )

    def test_create_full_issue_est(self):
        selectedApplOption = ApplOptions.objects.get(id=self.applOption.id)
        selectedApplOption = ApplOptions.objects.select_related('publoptions').get(id=self.applOption.id)
        UtilityApplication.objects.create_full(options=selectedApplOption, user=self.user)
        self.assertEquals(self.issue_template.official_cost,
                          IssueEst.objects.all().first().official_cost

        )
