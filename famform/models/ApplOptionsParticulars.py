from django.db import models

from characteristics.models import DocFormat
from famform.managers import ApplOptionsParticularsManager


class ApplOptionsParticulars(models.Model):
    request_examination_early_bool = models.BooleanField(default=False)
    doc_format = models.ForeignKey(DocFormat, on_delete=models.CASCADE)

    objects = ApplOptionsParticularsManager()
