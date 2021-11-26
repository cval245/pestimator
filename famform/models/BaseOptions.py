from django.db import models
from relativedeltafield import RelativeDeltaField

from famform.models.ApplOptions import ApplOptions


class BaseOptions(models.Model):
    date_diff = RelativeDeltaField()
    appl = models.OneToOneField(ApplOptions, on_delete=models.CASCADE)

    class Meta:
        abstract = True
