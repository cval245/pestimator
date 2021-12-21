from django.db import models

from famform.managers import ApplOptionsParticularsManager


class ApplOptionsParticulars(models.Model):
    request_examination_early_bool = models.BooleanField(default=False)
    doc_format = models.ForeignKey('characteristics.DocFormat', on_delete=models.CASCADE)

    objects = ApplOptionsParticularsManager()
