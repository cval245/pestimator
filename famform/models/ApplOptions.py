from django.db import models
from application.models import ApplDetails
from characteristics.enums import TranslationRequirements
from characteristics.models import Country, ApplType, TranslationImplementedPseudoEnum
from famform.managers import ApplOptionsManager
from famform.models.ApplOptionsParticulars import ApplOptionsParticulars
from famform.models.FamOptions import FamOptions
from transform.models import PublicationTransform, DefaultPublTransform, OATransform, DefaultOATransform, \
    AllowanceTransform, DefaultAllowanceTransform, IssueTransform, DefaultIssueTransform, RequestExaminationTransform, \
    DefaultRequestExaminationTransform


class ApplOptions(models.Model):
    title = models.TextField()
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    appl_type = models.ForeignKey(ApplType, on_delete=models.CASCADE)
    date_filing = models.DateField()
    # translation_full_required = models.BooleanField(default=False)
    translation_implemented = models.ForeignKey(TranslationImplementedPseudoEnum,
                                                on_delete=models.CASCADE,
                                                default=TranslationImplementedPseudoEnum.objects.get_name_from_enum(
                                                    TranslationRequirements.FULL_TRANSLATION).id)
    details = models.ForeignKey(ApplDetails, on_delete=models.CASCADE)
    fam_options = models.ForeignKey(FamOptions, on_delete=models.CASCADE)
    prev_appl_options = models.ForeignKey("self", on_delete=models.SET_NULL, null=True)
    particulars = models.OneToOneField(ApplOptionsParticulars, on_delete=models.CASCADE, null=False)

    objects = ApplOptionsManager()

    # prosecution_options = models.ForeignKey()

    def create_publ_option(self):
        if PublicationTransform.objects.filter(country=self.country).exists():
            trans = PublicationTransform.objects.get(country=self.country)
        else:
            trans = DefaultPublTransform.objects.get(appl_type=self.appl_type)

        from famform.models import PublOptions
        return PublOptions.objects.create(date_diff=trans.date_diff,
                                          appl=self)

    def create_examination(self, oa_total):
        self.create_request_examination_option()
        self.create_all_oa_options(oa_total)

    def create_request_examination_option(self):
        if RequestExaminationTransform.objects.filter(country=self.country).exists():
            trans = RequestExaminationTransform.objects.get(country=self.country)
        else:
            trans = DefaultRequestExaminationTransform.objects.get(appl_type=self.appl_type)
        from famform.models import RequestExaminationOptions
        return RequestExaminationOptions.objects.create(date_diff=trans.date_diff, appl=self)

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
        from famform.models import OAOptions
        return OAOptions.objects.create(date_diff=trans.date_diff, oa_prev=oa_prev, appl=self)

    def create_allow_option(self):
        if AllowanceTransform.objects.filter(country=self.country).exists():
            trans = AllowanceTransform.objects.get(country=self.country)
        else:
            trans = DefaultAllowanceTransform.objects.get(appl_type=self.appl_type)

        from famform.models import AllowOptions
        return AllowOptions.objects.create(date_diff=trans.date_diff, appl=self)

    def create_issue_option(self):
        if IssueTransform.objects.filter(country=self.country).exists():
            trans = IssueTransform.objects.get(country=self.country)
        else:
            trans = DefaultIssueTransform.objects.get(appl_type=self.appl_type)

        from famform.models import IssueOptions
        return IssueOptions.objects.create(date_diff=trans.date_diff, appl=self)
