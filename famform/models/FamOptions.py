import math
from copy import copy, deepcopy

from django.db import models

from application.models import ApplDetails
from characteristics.enums import ApplTypes, TranslationRequirements
from characteristics.models import ApplType
from famform.models.ApplOptions import ApplOptions
from famform.models.ApplOptionsParticulars import ApplOptionsParticulars
from famform.models.PCTApplOptions import PCTApplOptions
from family.models import Family
from pestimator.exceptions import ApplTypeNotAvailableForCountry, ISACountryNotAvailableForCountry
from transform.models import CountryOANum, CustomFilingTransform, DefaultCountryOANum


class FamOptions(models.Model):
    family = models.ForeignKey(Family, on_delete=models.CASCADE)

    def _calc_filing_date(self, appl_type, country, prev_appl_type, prev_date, prev_appl_option):

        date_filing = CustomFilingTransform.objects \
            .calc_filing_date_for_appl_option(appl_type=appl_type,
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
        new_pages = math.ceil(num_words / desired_language.words_per_page)

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
                          first_appl_bool, prev_appl_option, custom_options):
        pct_appl_type = ApplType.objects.get_name_from_enum(ApplTypes.PCT)
        particulars = ApplOptionsParticulars.objects.create_appl_options_particulars(
            custom_options=custom_options,
            country=country, appl_type=pct_appl_type)

        if isa_country not in country.isa_countries.all():
            raise ISACountryNotAvailableForCountry
        if pct_appl_type in country.available_appl_types.all():
            # select transform and get date_diff
            date_filing = self._calc_filing_date(pct_appl_type, country, prev_appl_type, prev_date, prev_appl_option)
            # get oa_total
            oa_total = self._calc_oa_num(country)

            det = self._smart_translate_details(
                country=country, details=details, appl_type=pct_appl_type,
                custom_details=custom_details, prev_appl_option=prev_appl_option)
            translated_details = det['translated_details']
            translation_enum = det['translation_enum']
            final_details = self.apply_custom_details(
                translated_details=translated_details,
                custom_details=custom_details)

            # apply transmutation transformations
            # these transmutations convert to local patent office guidelines
            # need user input
            # have defaults
            # ie transform multiple dependent claims into sets of single dependent claims

            pct_appl_option = PCTApplOptions.objects.create_pct_appl_option(
                date_filing=date_filing, country=country, details=final_details,
                oa_total=oa_total, fam_option=self, isa_country=isa_country,
                prev_appl_option=prev_appl_option,
                translation_enum=translation_enum,
                particulars=particulars,
            )
            return pct_appl_option

        else:
            raise ApplTypeNotAvailableForCountry

    def generate_appl(self, details, custom_details, country, appl_type, custom_options,
                      prev_appl_type, prev_date, first_appl_bool, prev_appl_option):

        # generate particulars from custom options
        particulars = ApplOptionsParticulars.objects.create_appl_options_particulars(
            custom_options=custom_options,
            country=country, appl_type=appl_type)
        # see if appl_type is valid for that country
        if appl_type in country.available_appl_types.all():
            # select transform and get date_diff
            date_filing = self._calc_filing_date(appl_type, country, prev_appl_type,
                                                 prev_date, prev_appl_option)
            # get oa_total
            oa_total = self._calc_oa_num(country)

            det = self._smart_translate_details(
                country=country, details=details, appl_type=appl_type,
                custom_details=custom_details, prev_appl_option=prev_appl_option)
            translated_details = det['translated_details']
            translation_enum = det['translation_enum']
            final_details = self.apply_custom_details(
                translated_details=translated_details,
                custom_details=custom_details)


            appl_option = ApplOptions.objects.create_appl_option(
                country=country,
                date_filing=date_filing,
                details=final_details,
                oa_total=oa_total,
                fam_option=self,
                translation_enum=translation_enum,
                appl_type=appl_type,
                particulars=particulars,
                prev_appl_option=prev_appl_option
            )
            return appl_option

        else:
            raise ApplTypeNotAvailableForCountry

    def apply_custom_details(self, translated_details, custom_details):
        final_details = copy(translated_details)
        # replace with custom details user provided on a key by key basis
        if custom_details is not None:
            for attr, value in custom_details.__dict__.items():
                if value is not None:
                    if attr != 'id':
                        setattr(final_details, attr, value)

        final_details.save()
        return final_details

    def determine_desired_language(self, details, country, appl_type, custom_details):
        # starting_languages
        if custom_details:
            if custom_details.language is not None:
                return custom_details.language

        destination_languages = country.available_languages.all()
        desired_language = destination_languages.get(languagecountry__default=True,
                                                     languagecountry__appl_type=appl_type)
        # override default language if there is option to keep in same language
        for lang in destination_languages:
            if lang == details.language:
                desired_language = lang

        return desired_language

    def _smart_translate_details(self, country, details, appl_type, custom_details, prev_appl_option):
        # determine if translation required
        desired_language = self.determine_desired_language(
            details=details, country=country,
            appl_type=appl_type, custom_details=custom_details,
        )
        old_language = None
        if prev_appl_option:
            prev_details = ApplDetails.objects.get(id=prev_appl_option.details.id)
            # old_language = prev_appl_option.details.language
            old_language = prev_details.language
        translate_enum = self.determine_extent_of_translation_required(
            country=country, appl_type=appl_type,
            old_language=old_language, new_language=desired_language)

        if translate_enum is TranslationRequirements.FULL_TRANSLATION:
            new_details = self.translate_details_new_language(
                details=details,
                current_language=details.language,
                desired_language=desired_language)
        elif translate_enum is TranslationRequirements.NO_TRANSLATION:
            new_details = deepcopy(details)
            new_details.pk = None
            new_details._state_adding = True
            new_details.save()
        else:
            # defaults to full translate
            new_details = self.translate_details_new_language(
                details=details,
                current_language=details.language,
                desired_language=desired_language)

        return {'translated_details': new_details, 'translation_enum': translate_enum}

    def determine_extent_of_translation_required(self, country, appl_type, old_language,
                                                 new_language):
        # determine if translations are required.
        if old_language == new_language:
            return TranslationRequirements.NO_TRANSLATION
        if appl_type.get_enum() is ApplTypes.EP_VALIDATION:
            if old_language.ep_official_language_bool:
                if country.ep_validation_translation_required.name == 'no translation required if official language':
                    return TranslationRequirements.NO_TRANSLATION
                elif country.ep_validation_translation_required.name == 'full translation required':
                    return TranslationRequirements.FULL_TRANSLATION
        return TranslationRequirements.FULL_TRANSLATION
