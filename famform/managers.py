from django.db import models

from characteristics.enums import ApplTypes
from characteristics.models import ApplType, TranslationImplementedPseudoEnum
from pestimator.exceptions import ApplTypePCTNotSupportedException, ApplTypePCTNationalPhaseNotSupportedException
from transform.models import PublicationTransform, DefaultPublTransform, AllowanceTransform, DefaultAllowanceTransform, \
    IssueTransform, DefaultIssueTransform, RequestExaminationTransform, DefaultRequestExaminationTransform, OATransform, \
    DefaultOATransform, USOATransform


class PCTApplOptionsManager(models.Manager):

    def create_pct_appl_option(self, date_filing, country, details,
                               oa_total, fam_option, isa_country,
                               isa_entity_size,
                               particulars,
                               translation_enum, prev_appl_option):
        pct_appl_type = ApplType.objects.get_name_from_enum(ApplTypes.PCT)
        pct_appl_option = self.create(title='title', date_filing=date_filing,
                                      country=country, appl_type=pct_appl_type,
                                      isa_country=isa_country,
                                      isa_entity_size=isa_entity_size,
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
            prev_appl_options=prev_appl_option)
        if appl_option.appl_type.get_enum() is ApplTypes.PROV:
            return appl_option
        elif appl_option.appl_type.get_enum() is ApplTypes.UTILITY:
            appl_option.create_publ_option()
            appl_option.create_examination(oa_total)
            appl_option.create_allow_option()
            appl_option.create_issue_option()
            return appl_option
        elif appl_option.appl_type.get_enum() is ApplTypes.EP:
            appl_option.create_publ_option()
            appl_option.create_examination(oa_total)
            appl_option.create_allow_option()
            return appl_option
        elif appl_option.appl_type.get_enum() is ApplTypes.EP_VALIDATION:
            appl_option.create_issue_option()
            return appl_option
        elif appl_option.appl_type.get_enum() is ApplTypes.PCT:
            raise ApplTypePCTNotSupportedException
            # raise ('PCT appltype cannot be used with ApplOptions, pass to PCTApplOptions Instead')
        elif appl_option.appl_type.get_enum() is ApplTypes.PCT_NATIONAL_PHASE:
            # raise ('PCTNationalPhase appltype cannot be used with ApplOptions')
            raise ApplTypePCTNationalPhaseNotSupportedException
        return appl_option


class ApplOptionsParticularsManager(models.Manager):
    def create_appl_options_particulars(self, custom_options, country, appl_type):
        if custom_options.doc_format is not None:
            doc_format = custom_options.doc_format
        else:
            doc_format = country.available_doc_formats \
                .get(docformatcountry__default=True, docformatcountry__appl_type=appl_type)
        particulars = self.create(
            doc_format=doc_format,
            request_examination_early_bool=custom_options.request_examination_early_bool)
        return particulars


class BaseOptionsManager(models.Manager):

    def create_option_with_class_names(self, Transform, DfltTransform, appl_option):
        country = appl_option.country
        appl_type = appl_option.appl_type
        prev_appl_option = appl_option.prev_appl_options
        prev_appl_type = None
        if prev_appl_option:
            prev_appl_type = prev_appl_option.appl_type

        if Transform.objects.filter(country=country, appl_type=appl_type).exists():
            if Transform.objects.filter(country=country, appl_type=appl_type, prev_appl_type=prev_appl_type).exists():
                trans = Transform.objects.get(country=country, appl_type=appl_type, prev_appl_type=prev_appl_type)
            elif Transform.objects.filter(country=country, appl_type=appl_type, prev_appl_type=None).exists():
                trans = Transform.objects.get(country=country, appl_type=appl_type, prev_appl_type=None)
            else:
                trans = DfltTransform.objects.get(appl_type=appl_type)
        else:
            trans = DfltTransform.objects.get(appl_type=appl_type)

        return self.create(date_diff=trans.date_diff, appl=appl_option)


class PublOptionsManager(BaseOptionsManager):
    def create_option(self, appl_option):
        return self.create_option_with_class_names(Transform=PublicationTransform,
                                                   DfltTransform=DefaultPublTransform,
                                                   appl_option=appl_option)


class AllowOptionsManager(BaseOptionsManager):
    def create_option(self, appl_option):
        return self.create_option_with_class_names(Transform=AllowanceTransform,
                                                   DfltTransform=DefaultAllowanceTransform,
                                                   appl_option=appl_option)


class IssueOptionsManager(BaseOptionsManager):
    def create_option(self, appl_option):
        return self.create_option_with_class_names(Transform=IssueTransform,
                                                   DfltTransform=DefaultIssueTransform,
                                                   appl_option=appl_option)


class RequestExaminationOptionsManager(BaseOptionsManager):
    def create_option(self, appl_option):
        return self.create_option_with_class_names(Transform=RequestExaminationTransform,
                                                   DfltTransform=DefaultRequestExaminationTransform,
                                                   appl_option=appl_option)


class OAOptionsManager(models.Manager):

    def create_option_with_class_names(self, Transform, DfltTransform, appl_option, oa_prev):
        country = appl_option.country
        appl_type = appl_option.appl_type

        prev_appl_option = appl_option.prev_appl_options
        prev_appl_type = None
        if prev_appl_option:
            prev_appl_type = prev_appl_option.appl_type

        if Transform.objects.filter(country=country, appl_type=appl_type).exists():
            if Transform.objects.filter(country=country, appl_type=appl_type, prev_appl_type=prev_appl_type).exists():
                trans = Transform.objects.get(country=country, appl_type=appl_type, prev_appl_type=prev_appl_type)
            elif Transform.objects.filter(country=country, appl_type=appl_type, prev_appl_type=None).exists():
                trans = Transform.objects.get(country=country, appl_type=appl_type, prev_appl_type=None)
            else:
                trans = DfltTransform.objects.get(appl_type=appl_type)
        else:
            trans = DfltTransform.objects.get(appl_type=appl_type)

        return self.create(date_diff=trans.date_diff, appl=appl_option, oa_prev=oa_prev)

    def create_option(self, appl_option, oa_prev):
        return self.create_option_with_class_names(Transform=OATransform,
                                                   DfltTransform=DefaultOATransform,
                                                   appl_option=appl_option,
                                                   oa_prev=oa_prev)

    def create_all_oa_options(self, appl_option, oa_total):
        i = 0
        oa_arr = []
        oa_prev = None
        while i < oa_total:
            oa = self.create_option(appl_option=appl_option, oa_prev=oa_prev)
            oa_prev = oa
            oa_arr.append(oa)
            i += 1
        return oa_arr


class USOAOptionsManager(models.Manager):

    def create_option_with_class_names(self, Transform, DfltTransform, appl_option, oa_prev, oa_final_bool):
        country = appl_option.country
        appl_type = appl_option.appl_type

        prev_appl_option = appl_option.prev_appl_options
        prev_appl_type = None
        if prev_appl_option:
            prev_appl_type = prev_appl_option.appl_type

        if Transform.objects.filter(country=country, appl_type=appl_type, oa_final_bool=oa_final_bool).exists():
            if Transform.objects.filter(country=country, appl_type=appl_type, prev_appl_type=prev_appl_type,
                                        oa_final_bool=oa_final_bool).exists():
                trans = Transform.objects.get(country=country, appl_type=appl_type, prev_appl_type=prev_appl_type,
                                              oa_final_bool=oa_final_bool)
            elif Transform.objects.filter(country=country, appl_type=appl_type, oa_final_bool=oa_final_bool,
                                          prev_appl_type=None).exists():
                trans = Transform.objects.get(country=country, appl_type=appl_type, oa_final_bool=oa_final_bool,
                                              prev_appl_type=None)
            else:
                trans = DfltTransform.objects.get(appl_type=appl_type)
        else:
            trans = DfltTransform.objects.get(appl_type=appl_type)

        return self.create(date_diff=trans.date_diff, appl=appl_option, oa_prev=oa_prev, oa_final_bool=oa_final_bool)

    def create_option(self, appl_option, oa_prev, oa_final_bool):
        return self.create_option_with_class_names(Transform=USOATransform,
                                                   DfltTransform=DefaultOATransform,
                                                   appl_option=appl_option,
                                                   oa_prev=oa_prev,
                                                   oa_final_bool=oa_final_bool)

    def create_all_oa_options(self, appl_option, oa_total):
        i = 0
        oa_arr = []
        oa_prev = None
        oa_final_bool = False
        while i < oa_total:
            oa = self.create_option(appl_option=appl_option, oa_prev=oa_prev, oa_final_bool=oa_final_bool)
            oa_prev = oa
            oa_arr.append(oa)
            oa_final_bool = not oa_final_bool
            i += 1
        return oa_arr
