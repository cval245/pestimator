from django.db import models

from characteristics.models import ApplType, TranslationImplementedPseudoEnum


class PCTApplOptionsManager(models.Manager):

    def create_pct_appl_option(self, date_filing, country, details,
                               oa_total, fam_option, isa_country, particulars,
                               translation_enum, prev_appl_option):
        pct_appl_type = ApplType.objects.get(application_type='pct')
        pct_appl_option = self.create(title='title', date_filing=date_filing,
                                      country=country, appl_type=pct_appl_type,
                                      isa_country=isa_country,
                                      details=details, fam_options=fam_option,
                                      translation_implemented=TranslationImplementedPseudoEnum.objects.get_name_from_enum(
                                          translation_enum),
                                      prev_appl_options=prev_appl_option,
                                      particulars=particulars)
        pct_appl_option.create_publ_option()
        pct_appl_option.create_examination(oa_total)
        return pct_appl_option


class ApplOptionsManager(models.Manager):

    def create_appl_option(self, date_filing, country, appl_type, details,
                           oa_total, fam_option, particulars,
                           translation_enum, prev_appl_option):
        appl_option = self.create(
            title='title', date_filing=date_filing,
            country=country, appl_type=appl_type,
            details=details, fam_options=fam_option,
            particulars=particulars,
            translation_implemented=TranslationImplementedPseudoEnum.objects.get_name_from_enum(translation_enum),
            prev_appl_options=prev_appl_option, )

        if (appl_option.appl_type == ApplType.objects.get(application_type='prov')):
            return appl_option
        elif (appl_option.appl_type == ApplType.objects.get(application_type='utility')):
            appl_option.create_publ_option()
            appl_option.create_examination(oa_total)
            appl_option.create_allow_option()
            appl_option.create_issue_option()
            return appl_option
        elif (appl_option.appl_type == ApplType.objects.get(application_type='ep')):
            appl_option.create_publ_option()
            appl_option.create_examination(oa_total)
            appl_option.create_allow_option()
            return appl_option
        elif (appl_option.appl_type == ApplType.objects.get(application_type='epvalidation')):
            appl_option.create_issue_option()
            return appl_option

        return appl_option


class ApplOptionsParticularsManager(models.Manager):
    def create_appl_options_particulars(self, custom_options, country, appl_type):
        doc_format = custom_options.doc_format
        if (custom_options.doc_format == None):
            doc_format = country.available_doc_formats \
                .get(docformatcountry__default=True, docformatcountry__appl_type=appl_type)
        particulars = self.create(
            doc_format=doc_format,
            request_examination_early_bool=custom_options.request_examination_early_bool)
        return particulars
