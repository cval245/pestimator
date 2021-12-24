from django.db import models

from famform.managers import ApplOptionsManager
from famform.models.RequestExaminationOptions import RequestExaminationOptions
from famform.models.AllowOptions import AllowOptions
from famform.models.IssueOptions import IssueOptions
from famform.models.OAOptions import OAOptions
from famform.models.PublOptions import PublOptions


class ApplOptions(models.Model):
    title = models.TextField()
    country = models.ForeignKey('characteristics.Country', on_delete=models.CASCADE)
    appl_type = models.ForeignKey('characteristics.ApplType', on_delete=models.CASCADE)
    date_filing = models.DateField()
    translation_implemented = models.ForeignKey(
        'characteristics.TranslationImplementedPseudoEnum',
        on_delete=models.CASCADE,
        default=2,
    )
    details = models.ForeignKey('application.ApplDetails', on_delete=models.CASCADE)
    fam_options = models.ForeignKey('FamOptions', on_delete=models.CASCADE)
    prev_appl_options = models.ForeignKey("self", on_delete=models.SET_NULL, null=True)
    particulars = models.OneToOneField('ApplOptionsParticulars', on_delete=models.CASCADE, null=False)

    objects = ApplOptionsManager()

    def create_examination(self, oa_total):
        self.create_request_examination_option()
        self.create_all_oa_options(oa_total)

    def create_publ_option(self):
        return PublOptions.objects.create_option(appl_option=self)

    def create_request_examination_option(self):
        return RequestExaminationOptions.objects.create_option(appl_option=self)

    def create_all_oa_options(self, oa_total):
        return OAOptions.objects.create_all_oa_options(appl_option=self,
                                                       oa_total=oa_total)

    def create_allow_option(self):
        return AllowOptions.objects.create_option(appl_option=self)

    def create_issue_option(self):
        return IssueOptions.objects.create_option(appl_option=self)
