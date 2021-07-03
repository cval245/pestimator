from django.db import models
from datetime import date
from application.models import ApplDetails
from relativedeltafield import RelativeDeltaField
from django.conf import settings
from characteristics.models import Country, EntitySize, ApplType
from family.models import Family
from anytree import Node, RenderTree, PreOrderIter, findall
from transform.models import DefaultFilingTransform, CustomFilingTransform,\
    IssueTransform, AllowanceTransform, OATransform, PublicationTransform, \
    CountryOANum, DefaultCountryOANum, DefaultPublTransform,\
    DefaultOATransform, DefaultAllowanceTransform, DefaultIssueTransform
# Create your models here.

class FamEstFormData(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    family = models.OneToOneField(Family, on_delete=models.CASCADE)
    countries = models.ManyToManyField(Country)
    init_appl_filing_date = models.DateField(default=date(2020, 1, 1))
    init_appl_country = models.ForeignKey(Country,
                                          on_delete=models.CASCADE,
                                          related_name='init_country')
    init_appl_type = models.ForeignKey(ApplType, on_delete=models.CASCADE)
    init_appl_indep_claims = models.IntegerField()
    init_appl_claims = models.IntegerField()
    init_appl_drawings = models.IntegerField()
    init_appl_pages = models.IntegerField()
    date_created = models.DateTimeField(auto_now_add=True)

    # change method to method_pct boolean
    # rename countries to method_pct_countries
    method = models.BooleanField(default=False)
    meth_country = models.ForeignKey(Country,
                                     on_delete=models.CASCADE,
                                     null=True,
                                     related_name='meth_country')
    # add method for paris treaty route
    # method_paris
    # method_paris_countries
    entity_size = models.ForeignKey(EntitySize, on_delete=models.CASCADE)

    # generate route
    
    def generate_family_options(self):
        famOptions = FamOptions.objects.create(family=self.family)
        init_appl_type = self.init_appl_type

        applDetails = ApplDetails.objects.create(
            num_indep_claims=self.init_appl_indep_claims,
            num_claims=self.init_appl_claims,
            num_drawings=self.init_appl_drawings,
            num_pages=self.init_appl_pages,
            entity_size=self.entity_size)

        # filing date is init_filing_date
        first_appl_bool = True
        famOptions.generate_appl(details=applDetails,
                                 country=self.init_appl_country,
                                 appl_type=self.init_appl_type,
                                 prev_appl_type=None,
                                 prev_date=self.init_appl_filing_date,
                                 first_appl_bool=first_appl_bool)

        # generate second node
        first_appl_bool = False
        prev_appl_type = init_appl_type
        prev_date = self.init_appl_filing_date
        if self.method is True and not init_appl_type.application_type == 'pct':
            pct_type = ApplType.objects.get(application_type='pct')
            applOption = famOptions.generate_appl(details=applDetails,
                                     country=self.meth_country,
                                     appl_type=pct_type,
                                     prev_appl_type=prev_appl_type,
                                     prev_date=prev_date,
                                     first_appl_bool=first_appl_bool)
            prev_date = applOption.date_filing
            prev_appl_type = pct_type

        # generate third node
        utility_appl = ApplType.objects.get(application_type='utility')
        countries = Country.objects.filter(famestformdata=self)
        for c in countries:
            famOptions.generate_appl(details=applDetails,
                                     country=c,
                                     appl_type=utility_appl,
                                     prev_appl_type=prev_appl_type,
                                     prev_date=prev_date,
                                     first_appl_bool=first_appl_bool)
        self.create_appls(famOptions)

    def create_appls(self, famOptions):
        # fam = Family.objects.get(id=self.family)
        fam = self.family
        print('fam', fam)
        fam.create_appls(famOptions)


class FamOptions(models.Model):
    family = models.ForeignKey(Family, on_delete=models.CASCADE)


    def _calc_filing_date(self, appl_type, country, prev_appl_type,
                          prev_date, first_appl_bool):
        if first_appl_bool:
            date_filing = prev_date
        else:
            custom_exists = CustomFilingTransform.objects.filter(
            appl_type=appl_type,
            country=country,
            prev_appl_type=prev_appl_type).exists()
            if custom_exists:
                cFilTrans = CustomFilingTransform.objects.get(
                    appl_type=appl_type,
                    country=country,
                    prev_appl_type=prev_appl_type)
                date_filing = prev_date + cFilTrans.date_diff
            else:
                dFilTrans = DefaultFilingTransform.objects.get(appl_type=appl_type)
                date_filing = prev_date + dFilTrans.date_diff

        return date_filing

    def _calc_oa_num(self, country):
        if CountryOANum.objects.filter(country=country).exists():
            oa_total = CountryOANum.objects.get(country=country).oa_total

        else:
            oa_total = DefaultCountryOANum.objects.first().oa_total

        return oa_total

    def generate_appl(self, details, country, appl_type,
                      prev_appl_type, prev_date, first_appl_bool):
        # select transform and get date_diff
        date_filing = self._calc_filing_date(appl_type, country,
                                             prev_appl_type, prev_date, first_appl_bool)
        # get oa_total
        oa_total = self._calc_oa_num(country)
        # calculate date_filing
        applOption = self.generate_appl_option(country=country,
                                               date_filing=date_filing,
                                               details=details,
                                               oa_total=oa_total,
                                               appl_type=appl_type)
        return applOption


    def generate_appl_option(self, country, details, appl_type,
                             date_filing, oa_total):
        applOption = ApplOptions.objects.create(title='title', date_filing=date_filing,
                                                country=country, appl_type=appl_type,
                                                details=details, fam_options=self)
        # select Transforms
        applOption.create_publ_option()
        applOption.create_all_oa_options(oa_total)
        applOption.create_allow_option()
        applOption.create_issue_option()
        return applOption


class ApplOptions(models.Model):
    title = models.TextField()
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    appl_type = models.ForeignKey(ApplType, on_delete=models.CASCADE)
    date_filing = models.DateField()
    details = models.ForeignKey(ApplDetails, on_delete=models.CASCADE)
    fam_options = models.ForeignKey(FamOptions, on_delete=models.CASCADE)
    prev_appl_options = models.ForeignKey("self", on_delete=models.SET_NULL, null=True)

    def create_publ_option(self):
        if PublicationTransform.objects.filter(country=self.country).exists():
            trans = PublicationTransform.objects.get(country=self.country)
        else:
            trans = DefaultPublTransform.objects.get(appl_type=self.appl_type)

        return PublOptions.objects.create(date_diff=trans.date_diff,
                                          appl=self)

    def create_all_oa_options(self, oa_tot):
        i = 0
        oa_arr = []
        oa_prev = None
        while i < oa_tot:
            oa = self.create_oa_option(oa_prev=oa_prev)
            oa_prev = oa
            oa_arr.append(oa)
            i += 1
        return oa_arr

    def create_oa_option(self, oa_prev):
        if OATransform.objects.filter(country=self.country).exists():
            trans = OATransform.objects.get(country=self.country)
        else:
            trans = DefaultOATransform.objects.get(appl_type=self.appl_type)

        return OAOptions.objects.create(date_diff=trans.date_diff, oa_prev=oa_prev, appl=self)

    def create_allow_option(self):
        if AllowanceTransform.objects.filter(country=self.country).exists():
            trans = AllowanceTransform.objects.get(country=self.country)
        else:
            trans = DefaultAllowanceTransform.objects.get(appl_type=self.appl_type)

        return AllowOptions.objects.create(date_diff=trans.date_diff, appl=self)

    def create_issue_option(self):
        if IssueTransform.objects.filter(country=self.country).exists():
            trans = IssueTransform.objects.get(country=self.country)
        else:
            trans = DefaultIssueTransform.objects.get(appl_type=self.appl_type)

        return IssueOptions.objects.create(date_diff=trans.date_diff, appl=self)


class BaseOptions(models.Model):
    date_diff = RelativeDeltaField()
    appl = models.OneToOneField(ApplOptions, on_delete=models.CASCADE)

    class Meta:
        abstract = True

class PublOptions(BaseOptions):

    class Meta:
        abstract = False

class OAOptions(BaseOptions):
    appl = models.ForeignKey(ApplOptions, on_delete=models.CASCADE)
    oa_prev = models.ForeignKey('self', models.SET_NULL, null=True)

    class Meta:
        abstract = False

class AllowOptions(BaseOptions):

    class Meta:
        abstract = False

class IssueOptions(BaseOptions):

    class Meta:
        abstract = False

