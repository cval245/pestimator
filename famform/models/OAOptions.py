from django.db import models
from relativedeltafield import RelativeDeltaField

from famform.managers import OAOptionsManager


class OAOptions(models.Model):
    date_diff = RelativeDeltaField()
    appl = models.ForeignKey('ApplOptions', on_delete=models.CASCADE)
    oa_prev = models.ForeignKey('self', models.SET_NULL, null=True)

    objects = OAOptionsManager()
