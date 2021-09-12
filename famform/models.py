from datetime import date

from django.conf import settings
from django.db import models
from django.db.models import Sum
from relativedeltafield import RelativeDeltaField

from application.models import ApplDetails
from characteristics.models import Country, EntitySize, ApplType
from family.models import Family
from transform.models import DefaultFilingTransform, CustomFilingTransform, \
    IssueTransform, AllowanceTransform, OATransform, PublicationTransform, \
    CountryOANum, DefaultCountryOANum, DefaultPublTransform, \
    DefaultOATransform, DefaultAllowanceTransform, DefaultIssueTransform


# Create your models here.

class FamEstFormData(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    family = models.OneToOneField(Family, on_delete=models.CASCADE)
    countries = models.ManyToManyField(Country)  # utility appl countries
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

    ep_method = models.BooleanField(default=False)
    # ep_countries = models.ManyToManyField(Country, null=True) # utility appl countries
    # add method for paris treaty route
    # method_paris
    # method_paris_countries
    entity_size = models.ForeignKey(EntitySize, on_delete=models.CASCADE)

    # generate route

    def generate_family_options(self):
        famOptions = FamOptions.objects.create(family=self.family)
        init_appl_type = self.init_appl_type
        # todo handlue multiple instead of just first opitionally add for user
        language = self.init_appl_country.languages_set.first()

        applDetails = ApplDetails.objects.create(
            num_indep_claims=self.init_appl_indep_claims,
            num_claims=self.init_appl_claims,
            num_pages_drawings=self.init_appl_drawings,
            num_pages=self.init_appl_pages,
            entity_size=self.entity_size,
            language_id=language.id
        )

        # filing date is init_filing_date
        first_appl_bool = True
        prevApplOption = None
        prov_appl_option = famOptions.generate_appl(details=applDetails,
                                                    country=self.init_appl_country,
                                                    appl_type=self.init_appl_type,
                                                    prev_appl_type=None,
                                                    prev_date=self.init_appl_filing_date,
                                                    first_appl_bool=first_appl_bool,
                                                    prev_appl_option=prevApplOption)

        # generate second node
        first_appl_bool = False
        prev_appl_type = init_appl_type
        prev_date = self.init_appl_filing_date
        prevApplOption = prov_appl_option
        if self.method is True and not init_appl_type.application_type == 'pct':
            pct_type = ApplType.objects.get(application_type='pct')
            applOption = famOptions.generate_appl(details=applDetails,
                                                  country=self.meth_country,
                                                  appl_type=pct_type,
                                                  prev_appl_type=prev_appl_type,
                                                  prev_date=prev_date,
                                                  first_appl_bool=first_appl_bool,
                                                  prev_appl_option=prevApplOption)
            prev_date = applOption.date_filing
            prev_appl_type = pct_type
            prevApplOption = applOption
        # generate ep method
        countries = Country.objects.filter(famestformdata=self)
        if self.ep_method is True:
            ep_applType = ApplType.objects.get(application_type='ep')
            epAppl = famOptions.generate_appl(details=applDetails,
                                              country=Country.objects.get(country='EP'),
                                              appl_type=ep_applType,
                                              prev_appl_type=prev_appl_type,
                                              prev_date=prev_date,
                                              first_appl_bool=first_appl_bool,
                                              prev_appl_option=prevApplOption)
            epPrevApplOption = epAppl

            # calc date of allowance
            oa_diff = OAOptions.objects.filter(appl=epAppl).aggregate(date_diff=Sum('date_diff'))['date_diff']
            allow_diff = AllowOptions.objects.get(appl=epAppl).date_diff
            ep_prev_date = prev_date + oa_diff + allow_diff
            ep_countries = countries.filter(ep_bool=True)
            countries = countries.exclude(ep_bool=True)
            ep_validation_appl = ApplType.objects.get(application_type='epvalidation')
            for c in ep_countries:
                famOptions.generate_appl(details=applDetails,
                                         country=c,
                                         appl_type=ep_validation_appl,
                                         prev_appl_type=prev_appl_type,
                                         prev_date=ep_prev_date,
                                         first_appl_bool=first_appl_bool,
                                         prev_appl_option=epPrevApplOption)

            # create utility applications where country is EP

        # generate third node
        utility_appl = ApplType.objects.get(application_type='utility')
        for c in countries:
            famOptions.generate_appl(details=applDetails,
                                     country=c,
                                     appl_type=utility_appl,
                                     prev_appl_type=prev_appl_type,
                                     prev_date=prev_date,
                                     first_appl_bool=first_appl_bool,
                                     prev_appl_option=prevApplOption)

        self.create_appls(famOptions)

    def create_appls(self, famOptions):
        # fam = Family.objects.get(id=self.family)
        fam = self.family
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

    def translate_details_new_language(self, details, current_language, desired_language):
        # convert current language to english ex. French to English
        num_words = current_language.words_per_page * details.num_pages
        new_pages = num_words / desired_language.words_per_page

        new_details = ApplDetails.objects.create(
            num_indep_claims=details.num_indep_claims,
            num_pages=new_pages,
            num_claims=details.num_claims,
            num_pages_drawings=details.num_pages_drawings,
            entity_size=details.entity_size,
            language_id=desired_language.id
        )
        return new_details

    def generate_appl(self, details, country, appl_type,
                      prev_appl_type, prev_date, first_appl_bool, prev_appl_option):
        # select transform and get date_diff
        date_filing = self._calc_filing_date(appl_type, country,
                                             prev_appl_type, prev_date, first_appl_bool)
        # get oa_total
        oa_total = self._calc_oa_num(country)

        # apply translations transformations
        # these translations lookup conversions from one language to another
        # words per page default for language
        # converting from one to another
        destination_languages = country.languages_set.all()
        desired_language = destination_languages.first()
        for lang in destination_languages:
            if (lang == details.language):
                desired_language = lang

        translated_details = self.translate_details_new_language(
            details=details,
            current_language=details.language,
            desired_language=desired_language, )

        # apply transmutation transformations
        # these transmutations convert to local patent office guidelines
        # need user input
        # have defaults
        # ie transform multiple dependent claims into sets of single dependent claims

        applOption = self.generate_appl_option(country=country,
                                               date_filing=date_filing,
                                               details=translated_details,
                                               oa_total=oa_total,
                                               appl_type=appl_type,
                                               prev_appl_option=prev_appl_option)
        return applOption

    def generate_appl_option(self, country, details, appl_type,
                             date_filing, oa_total, prev_appl_option):
        applOption = ApplOptions.objects.create(title='title', date_filing=date_filing,
                                                country=country, appl_type=appl_type,
                                                details=details, fam_options=self,
                                                prev_appl_options=prev_appl_option)
        # select Transforms
        if (applOption.appl_type == ApplType.objects.get(application_type='prov')):
            return applOption
        elif (applOption.appl_type == ApplType.objects.get(application_type='pct')):
            applOption.create_publ_option()
            return applOption
        elif (applOption.appl_type == ApplType.objects.get(application_type='utility')):
            applOption.create_publ_option()
            applOption.create_all_oa_options(oa_total)
            applOption.create_allow_option()
            applOption.create_issue_option()
            return applOption
        elif (applOption.appl_type == ApplType.objects.get(application_type='ep')):
            applOption.create_publ_option()
            applOption.create_all_oa_options(oa_total)
            applOption.create_allow_option()
            return applOption
        elif (applOption.appl_type == ApplType.objects.get(application_type='epvalidation')):
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

class OAOptions(models.Model):
    date_diff = RelativeDeltaField()
    appl = models.ForeignKey(ApplOptions, on_delete=models.CASCADE)
    oa_prev = models.ForeignKey('self', models.SET_NULL, null=True)


class AllowOptions(BaseOptions):

    class Meta:
        abstract = False

class IssueOptions(BaseOptions):

    class Meta:
        abstract = False
