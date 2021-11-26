from copy import deepcopy

from django.db import models

from application.models import ApplDetails
from characteristics.models import ApplType, EPValidationTranslationRequired
# from famform.models import PCTApplOptions, ApplOptions
from family.models import Family
from transform.models import CustomFilingTransform, CountryOANum, DefaultCountryOANum


class FamOptions(models.Model):
    family = models.ForeignKey(Family, on_delete=models.CASCADE)

    def _calc_filing_date(self, appl_type, country, prev_appl_type,
                          prev_date, first_appl_bool, prev_appl_option):

        date_filing = CustomFilingTransform.objects.calc_filing_date_for_appl_option(appl_type=appl_type,
                                                                                     country=country,
                                                                                     prev_appl_type=prev_appl_type,
                                                                                     prev_date=prev_date,
                                                                                     prev_appl_option=prev_appl_option)
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
            num_claims_multiple_dependent=details.num_claims_multiple_dependent,
            num_drawings=details.num_drawings,
            num_pages_description=new_pages,
            num_pages_claims=details.num_pages_claims,
            num_pages_drawings=details.num_pages_drawings,
            entity_size=details.entity_size,
            language_id=desired_language.id
        )
        return new_details

    def generate_pct_appl(self, details, custom_details, country, isa_country, prev_appl_type, prev_date,
                          first_appl_bool, prev_appl_option):
        pct_appl_type = ApplType.objects.get(application_type='pct')
        if (isa_country not in country.isa_countries.all()):
            raise 'isa country needs to be available for country'
        if pct_appl_type in country.available_appl_types.all():
            # select transform and get date_diff
            date_filing = self._calc_filing_date(pct_appl_type, country,
                                                 prev_appl_type, prev_date, first_appl_bool, prev_appl_option)
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
                translated_details = deepcopy(details)
                translated_details.pk = None
                translated_details._state_adding = True
                translated_details.save()

            final_details = self.apply_custom_details(
                translated_details=translated_details,
                custom_details=custom_details)
            # apply transmutation transformations
            # these transmutations convert to local patent office guidelines
            # need user input
            # have defaults
            # ie transform multiple dependent claims into sets of single dependent claims
            applOption = self.generate_pct_appl_option(country=country,
                                                       isa_country=isa_country,
                                                       date_filing=date_filing,
                                                       details=final_details,
                                                       oa_total=oa_total,
                                                       translation_full_required=translation_full_required,
                                                       prev_appl_option=prev_appl_option)
            return applOption
        else:
            raise 'Error: ApplType not available for country'

    def generate_appl(self, details, custom_details, country, appl_type,
                      prev_appl_type, prev_date, first_appl_bool, prev_appl_option):
        # see if appl_type is valid for that country
        if (appl_type in country.available_appl_types.all()):

            # select transform and get date_diff
            date_filing = self._calc_filing_date(appl_type, country,
                                                 prev_appl_type, prev_date, first_appl_bool, prev_appl_option)
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
                translated_details = deepcopy(details)
                translated_details.pk = None
                translated_details._state_adding = True
                translated_details.save()

            final_details = self.apply_custom_details(
                translated_details=translated_details,
                custom_details=custom_details)
            if (custom_details):
                print('custom_details', custom_details.__dict__)
                print('after custom_details', final_details.__dict__)
            # apply transmutation transformations
            # these transmutations convert to local patent office guidelines
            # need user inpu
            # have defaults
            # ie transform multiple dependent claims into sets of single dependent claims

            applOption = self.generate_appl_option(country=country,
                                                   date_filing=date_filing,
                                                   details=final_details,
                                                   oa_total=oa_total,
                                                   translation_full_required=translation_full_required,
                                                   appl_type=appl_type,
                                                   prev_appl_option=prev_appl_option)
            return applOption
        else:
            print(appl_type.application_type,
                  '<+ appl type  country=>  ', country.country)
            raise 'Error: ApplType not available for country'

    def apply_custom_details(self, translated_details, custom_details):
        final_details = translated_details
        # replace with custom details user provided on a key by key basis
        if custom_details is not None:
            for attr, value in custom_details.__dict__.items():
                if value is not None:
                    if attr != 'id':
                        setattr(final_details, attr, value)
                    # final_details[attr] = value

        final_details.save()
        return final_details

    def determine_translation_full_required(self, country, appl_type, language, prev_appl_option):
        # determine if translations are required.
        translation_full_required = True;
        if (appl_type == ApplType.objects.get(application_type='epvalidation')):
            # epvalidation countries behave weirdly
            if (country.ep_validation_translation_required
                    == EPValidationTranslationRequired.objects.get(name='No Translation required')):
                translation_full_required = False
        elif (prev_appl_option):
            print('prev_appl_option.details', vars(prev_appl_option.details))
            if (language.id == prev_appl_option.details.language_id):
                print('prev_appl_option.details.langauge', prev_appl_option.details.language_id)
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
        from famform.models import PCTApplOptions
        applOption = PCTApplOptions.objects.create(title='title', date_filing=date_filing,
                                                   country=country, appl_type=pct_appl_type,
                                                   isa_country=isa_country,
                                                   details=details, fam_options=self,
                                                   translation_full_required=translation_full_required,
                                                   prev_appl_options=prev_appl_option)
        applOption.create_publ_option()
        applOption.create_examination(oa_total)
        # applOption.create_request_examination_option()
        return applOption

    def generate_appl_option(self, country, details, appl_type,
                             translation_full_required,
                             date_filing, oa_total, prev_appl_option):
        from famform.models import ApplOptions
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
            # applOption.create_all_oa_options(oa_total)
            applOption.create_examination(oa_total)
            applOption.create_allow_option()
            applOption.create_issue_option()
            return applOption
        elif (applOption.appl_type == ApplType.objects.get(application_type='ep')):
            applOption.create_publ_option()
            applOption.create_examination(oa_total)
            # applOption.create_all_oa_options(oa_total)
            applOption.create_allow_option()
            return applOption
        elif (applOption.appl_type == ApplType.objects.get(application_type='epvalidation')):
            applOption.create_issue_option()
            return applOption
