from datetime import date

from django.conf import settings
from django.db import models
from django.db.models import Sum, Max
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
    unique_display_no = models.IntegerField()
    init_appl_filing_date = models.DateField(default=date(2020, 1, 1))
    init_appl_country = models.ForeignKey(Country,
                                          on_delete=models.CASCADE,
                                          related_name='init_country')
    init_appl_type = models.ForeignKey(ApplType, on_delete=models.CASCADE)
    init_appl_indep_claims = models.IntegerField()
    init_appl_claims = models.IntegerField()
    init_appl_drawings = models.IntegerField()
    # init_appl_pages = models.IntegerField()
    init_appl_pages_desc = models.IntegerField()
    init_appl_pages_drawings = models.IntegerField()
    init_appl_pages_claims = models.IntegerField()
    date_created = models.DateTimeField(auto_now_add=True)

    # change method to method_pct boolean
    # rename countries to method_pct_countries
    pct_method = models.BooleanField(default=False)
    pct_country = models.ForeignKey(Country,
                                    on_delete=models.CASCADE,
                                    null=True,
                                    related_name='pct_country')
    isa_country = models.ForeignKey(Country,
                                    on_delete=models.CASCADE,
                                    null=True,
                                    related_name='isa_country')
    pct_countries = models.ManyToManyField(Country, related_name='pct_countries')  # utility appl countries

    ep_method = models.BooleanField(default=False)
    ep_countries = models.ManyToManyField(Country, related_name='ep_countries')  # utility appl countries

    paris_countries = models.ManyToManyField(Country, related_name='paris_countries')  # utility appl countries
    entity_size = models.ForeignKey(EntitySize, on_delete=models.CASCADE)

    # generate route
    def save(self, *args, **kwargs):
        if self.pk == None:
            # get all pervious families by user
            max_udn = FamEstFormData.objects.filter(user=self.user).aggregate(max_udn=Max('unique_display_no'))
            if max_udn['max_udn'] is not None:
                self.unique_display_no = max_udn['max_udn'] + 1
            else:
                self.unique_display_no = 1
        return super(FamEstFormData, self).save(*args, **kwargs)

    def generate_family_options(self):
        famOptions = FamOptions.objects.create(family=self.family)
        # !important the ep application must be added in either first appl
        # or paris appls or pct appls
        # todo handlue multiple instead of just first opitionally add for user
        language = self.init_appl_country.languages_set.first()

        applDetails = ApplDetails.objects.create(
            num_indep_claims=self.init_appl_indep_claims,
            num_claims=self.init_appl_claims,
            num_drawings=self.init_appl_drawings,
            num_pages_drawings=self.init_appl_pages_drawings,
            num_pages_claims=self.init_appl_pages_claims,
            num_pages_description=self.init_appl_pages_desc,
            entity_size=self.entity_size,
            language_id=language.id
        )

        init_appl_option = self.parse_first_appl_stage(famOptions, applDetails)
        if (self.init_appl_type != ApplType.objects.get(application_type='pct')
                and self.pct_method is True):
            self.parse_international_stage(famOptions=famOptions,
                                           applDetails=applDetails,
                                           prevApplOption=init_appl_option,
                                           firstApplBool=False,
                                           prevDate=init_appl_option.date_filing,
                                           prevApplType=self.init_appl_type)

        self.parse_paris_stage(famOptions=famOptions, applDetails=applDetails,
                               prevApplOption=init_appl_option)
        self.family.create_appls(famOptions)

    def parse_first_appl_stage(self, famOptions, applDetails):
        # take in first appl
        # if ep, then commence
        # parse_ep_stage()
        print('asdfasghs', ApplType.objects.get(application_type='pct'))
        if self.init_appl_type == ApplType.objects.get(application_type='pct'):
            print('asdfasghs', ApplType.objects.get(application_type='pct'))
            first_appl_option = self.parse_international_stage(famOptions=famOptions,
                                                               applDetails=applDetails,
                                                               prevApplOption=None,
                                                               prevDate=self.init_appl_filing_date,
                                                               prevApplType=self.init_appl_type,
                                                               firstApplBool=True)

        elif self.init_appl_type == ApplType.objects.get(application_type='ep'):
            first_appl_option = self.parse_ep_stage(famOptions=famOptions,
                                                    applDetails=applDetails,
                                                    prevApplOption=None,
                                                    firstApplBool=True,
                                                    prev_date=self.init_appl_filing_date,
                                                    prev_appl_type=self.init_appl_type,
                                                    )

        else:
            first_appl_option = famOptions.generate_appl(details=applDetails,
                                                         country=self.init_appl_country,
                                                         appl_type=self.init_appl_type,
                                                         prev_appl_type=None,
                                                         prev_date=self.init_appl_filing_date,
                                                         first_appl_bool=True,
                                                         prev_appl_option=None)
        print('first_appl_option', first_appl_option)
        return first_appl_option

    def parse_international_stage(self, famOptions, applDetails,
                                  prevApplOption, prevDate, prevApplType, firstApplBool):
        if (self.pct_method is True):
            # take in pct_countries
            # check if ep stage is also checked
            # check if first appl was ep
            # if yes and then no, create ep option
            # if ep first was checked then get nothing
            pct_valid_type = ApplType.objects.get(application_type='pct')
            print('parsing inter stage')
            pct_appl_option = famOptions.generate_pct_appl(details=applDetails,
                                                           country=self.pct_country,
                                                           isa_country=self.isa_country,
                                                           # appl_type=pct_valid_type,
                                                           prev_appl_type=prevApplType,
                                                           prev_date=prevDate,
                                                           first_appl_bool=firstApplBool,
                                                           prev_appl_option=prevApplOption)

            print('parsing inter stage', pct_appl_option)
            utility_type = ApplType.objects.get(application_type='utility')
            for c in self.pct_countries.all():
                if (c == Country.objects.get(country='EP')
                        and self.ep_method is True
                        and self.init_appl_type != ApplType.objects.get(application_type='ep')):
                    self.parse_ep_stage(famOptions=famOptions,
                                        applDetails=applDetails,
                                        prevApplOption=pct_appl_option,
                                        firstApplBool=False,
                                        prev_date=pct_appl_option.date_filing,
                                        prev_appl_type=pct_valid_type)
                else:
                    famOptions.generate_appl(details=applDetails,
                                             country=c,
                                             appl_type=utility_type,
                                             prev_appl_type=pct_valid_type,
                                             prev_date=pct_appl_option.date_filing,
                                             first_appl_bool=False,
                                             prev_appl_option=pct_appl_option)
            return pct_appl_option
        return prevApplOption

    def parse_ep_stage(self, famOptions, applDetails, prevApplOption, firstApplBool, prev_date, prev_appl_type):
        # take in ep_countries
        # check if pct countries apply
        if (self.ep_method is True):
            ep_type = ApplType.objects.get(application_type='ep')
            ep_country = Country.objects.get(country='EP')
            ep_appl_option = famOptions.generate_appl(details=applDetails,
                                                      country=ep_country,
                                                      appl_type=ep_type,
                                                      prev_appl_type=prev_appl_type,
                                                      prev_date=prev_date,
                                                      first_appl_bool=firstApplBool,
                                                      prev_appl_option=prevApplOption)
            self.parse_ep_validation_stage(famOptions=famOptions,
                                           applDetails=applDetails,
                                           prevApplOption=ep_appl_option)
            return ep_appl_option

    def parse_ep_validation_stage(self, famOptions, applDetails, prevApplOption):

        ep_valid_type = ApplType.objects.get(application_type='epvalidation')
        oa_diff = OAOptions.objects.filter(appl=prevApplOption).aggregate(date_diff=Sum('date_diff'))['date_diff']
        allow_diff = AllowOptions.objects.get(appl=prevApplOption).date_diff
        # TODO this is messy replace options with dates from diffs
        ep_prev_date = prevApplOption.date_filing + oa_diff + allow_diff
        for c in self.ep_countries.all():
            famOptions.generate_appl(details=applDetails,
                                     country=c,
                                     appl_type=ep_valid_type,
                                     prev_appl_type=prevApplOption.appl_type,
                                     prev_date=ep_prev_date,
                                     first_appl_bool=False,
                                     prev_appl_option=prevApplOption)

    def parse_paris_stage(self, famOptions, applDetails, prevApplOption):
        # take in paris_countries
        utility_appl = ApplType.objects.get(application_type='utility')
        for c in self.paris_countries.all():
            if (c == Country.objects.get(country='EP')
                    and self.ep_method is True):
                self.parse_ep_stage(famOptions=famOptions,
                                    applDetails=applDetails,
                                    prevApplOption=prevApplOption.date_filing,
                                    firstApplBool=False)
            else:
                famOptions.generate_appl(details=applDetails,
                                         country=c,
                                         appl_type=utility_appl,
                                         prev_appl_type=prevApplOption.appl_type,
                                         prev_date=prevApplOption.date_filing,
                                         first_appl_bool=False,
                                         prev_appl_option=prevApplOption)


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
        num_words = current_language.words_per_page * details.num_pages_description
        new_pages = num_words / desired_language.words_per_page

        new_details = ApplDetails.objects.create(
            num_indep_claims=details.num_indep_claims,
            num_claims=details.num_claims,
            num_drawings=details.num_drawings,
            num_pages_description=new_pages,
            num_pages_claims=details.num_pages_claims,
            num_pages_drawings=details.num_pages_drawings,
            entity_size=details.entity_size,
            language_id=desired_language.id
        )
        return new_details

    def generate_pct_appl(self, details, country, isa_country, prev_appl_type, prev_date,
                          first_appl_bool, prev_appl_option):
        pct_appl_type = ApplType.objects.get(application_type='pct')
        if (isa_country not in country.isa_countries):
            raise 'isa country needs to be available for country'
        if pct_appl_type in country.available_appl_types.all():
            # select transform and get date_diff
            date_filing = self._calc_filing_date(pct_appl_type, country,
                                                 prev_appl_type, prev_date, first_appl_bool)
            # get oa_total
            oa_total = self._calc_oa_num(country)

            desired_language = self.determine_desired_language(
                details=details, country=country,
            )
            translation_full_required = self.determine_translation_full_required(
                country=country,
                appl_type=pct_appl_type,
                language=desired_language,
                prev_appl_option=prev_appl_option)

            if (translation_full_required):
                translated_details = self.translate_details_new_language(
                    details=details,
                    current_language=details.language,
                    desired_language=desired_language)
            else:
                translated_details = details
                translated_details.pk = None
                translated_details.save()

            # apply transmutation transformations
            # these transmutations convert to local patent office guidelines
            # need user input
            # have defaults
            # ie transform multiple dependent claims into sets of single dependent claims

            applOption = self.generate_pct_appl_option(country=country,
                                                       isa_country=isa_country,
                                                       date_filing=date_filing,
                                                       details=translated_details,
                                                       oa_total=oa_total,
                                                       translation_full_required=translation_full_required,
                                                       prev_appl_option=prev_appl_option)
            return applOption
        else:
            raise 'Error: ApplType not available for country'

    def generate_appl(self, details, country, appl_type,
                      prev_appl_type, prev_date, first_appl_bool, prev_appl_option):
        # see if appl_type is valid for that country
        if (appl_type in country.available_appl_types.all()):

            # select transform and get date_diff
            date_filing = self._calc_filing_date(appl_type, country,
                                                 prev_appl_type, prev_date, first_appl_bool)
            # get oa_total
            oa_total = self._calc_oa_num(country)

            # apply translations transformations
            # these translations lookup conversions from one language to another
            # words per page default for language
            # converting from one to another
            desired_language = self.determine_desired_language(
                details=details, country=country,
            )
            translation_full_required = self.determine_translation_full_required(
                country=country,
                appl_type=appl_type,
                language=desired_language,
                prev_appl_option=prev_appl_option)

            if (translation_full_required):
                translated_details = self.translate_details_new_language(
                    details=details,
                    current_language=details.language,
                    desired_language=desired_language)
            else:
                translated_details = details
                translated_details.pk = None
                translated_details.save()

            # apply transmutation transformations
            # these transmutations convert to local patent office guidelines
            # need user input
            # have defaults
            # ie transform multiple dependent claims into sets of single dependent claims

            applOption = self.generate_appl_option(country=country,
                                                   date_filing=date_filing,
                                                   details=translated_details,
                                                   oa_total=oa_total,
                                                   translation_full_required=translation_full_required,
                                                   appl_type=appl_type,
                                                   prev_appl_option=prev_appl_option)
            return applOption
        else:
            print(appl_type.application_type,
                  '<+ appl type  country=>  ', country.country)
            raise 'Error: ApplType not available for country'

    def determine_translation_full_required(self, country, appl_type, language, prev_appl_option):
        # determine if translations are required.
        translation_full_required = True;
        if (appl_type == ApplType.objects.get(application_type='epvalidation')):
            # epvalidation countries behave weirdly
            if ((country == Country.objects.get(country='GB'))
                    | (country == Country.objects.get(country='FR'))
                    | (country == Country.objects.get(country='DE'))
            ):
                translation_full_required = False
        elif (prev_appl_option):
            if (language == prev_appl_option.details.language):
                # same languages don't require translation
                translation_full_required = False
        return translation_full_required

    def determine_desired_language(self, details, country):
        # starting_langagues
        destination_languages = country.languages_set.all()
        desired_language = destination_languages.first()
        for lang in destination_languages:
            if (lang == details.language):
                desired_language = lang

        return desired_language

    def generate_pct_appl_option(self, country, isa_country, translation_full_required,
                                 date_filing, oa_total, prev_appl_option, details):
        pct_appl_type = ApplType.objects.get(application_type='pct')
        applOption = PCTApplOptions.objects.create(title='title', date_filing=date_filing,
                                                   country=country, appl_type=pct_appl_type,
                                                   isa_country=isa_country,
                                                   details=details, fam_options=self,
                                                   translation_full_required=translation_full_required,
                                                   prev_appl_options=prev_appl_option)
        applOption.create_publ_option()
        return applOption

    def generate_appl_option(self, country, details, appl_type,
                             translation_full_required,
                             date_filing, oa_total, prev_appl_option):
        applOption = ApplOptions.objects.create(title='title', date_filing=date_filing,
                                                country=country, appl_type=appl_type,
                                                details=details, fam_options=self,
                                                translation_full_required=translation_full_required,
                                                prev_appl_options=prev_appl_option)
        # select Transforms
        if (applOption.appl_type == ApplType.objects.get(application_type='prov')):
            return applOption
        # elif (applOption.appl_type == ApplType.objects.get(application_type='pct')):
        #     applOption.create_publ_option()
        #     return applOption
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
    translation_full_required = models.BooleanField(default=False)
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


class PCTApplOptions(ApplOptions):
    isa_country = models.ForeignKey(Country, on_delete=models.CASCADE)


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
