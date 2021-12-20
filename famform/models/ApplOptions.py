from django.db import models
from application.models import ApplDetails
from characteristics.models import Country, ApplType, TranslationImplementedPseudoEnum
from famform.managers import ApplOptionsManager
from famform.models.ApplOptionsParticulars import ApplOptionsParticulars
from famform.models.FamOptions import FamOptions



class ApplOptions(models.Model):
    title = models.TextField()
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    appl_type = models.ForeignKey(ApplType, on_delete=models.CASCADE)
    date_filing = models.DateField()
    translation_implemented = models.ForeignKey(
        TranslationImplementedPseudoEnum,
        on_delete=models.CASCADE,
        default=2,
        # default=TranslationImplementedPseudoEnum.objects.get_name_from_enum(
        #     TranslationRequirements.FULL_TRANSLATION).id
    )
    details = models.ForeignKey(ApplDetails, on_delete=models.CASCADE)
    fam_options = models.ForeignKey(FamOptions, on_delete=models.CASCADE)
    prev_appl_options = models.ForeignKey("self", on_delete=models.SET_NULL, null=True)
    particulars = models.OneToOneField(ApplOptionsParticulars, on_delete=models.CASCADE, null=False)

    objects = ApplOptionsManager()

    def create_examination(self, oa_total):
        self.create_request_examination_option()
        self.create_all_oa_options(oa_total)

    def create_publ_option(self):
        from famform.models import PublOptions
        return PublOptions.objects.create_option(appl_option=self)

    def create_request_examination_option(self):
        from famform.models import RequestExaminationOptions
        return RequestExaminationOptions.objects.create_option(appl_option=self)

    def create_all_oa_options(self, oa_total):
        from famform.models import OAOptions
        return OAOptions.objects.create_all_oa_options(appl_option=self,
                                                       oa_total=oa_total)

    def create_allow_option(self):
        from famform.models import AllowOptions
        return AllowOptions.objects.create_option(appl_option=self)

    def create_issue_option(self):
        from famform.models import IssueOptions
        return IssueOptions.objects.create_option(appl_option=self)
