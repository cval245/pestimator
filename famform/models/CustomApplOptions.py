from django.db import models

from characteristics.models import DocFormat


class CustomApplOptions(models.Model):
    request_examination_early_bool = models.BooleanField(default=False)
    doc_format = models.ForeignKey(DocFormat, on_delete=models.CASCADE, default=None, null=True)
