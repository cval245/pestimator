from django.db import models
from relativedeltafield import RelativeDeltaField

from famform.managers import BaseOptionsManager


# from famform.models import ApplOptions


class BaseOptions(models.Model):
    date_diff = RelativeDeltaField()
    appl = models.OneToOneField('ApplOptions', on_delete=models.CASCADE)

    objects = BaseOptionsManager()

    class Meta:
        abstract = True
