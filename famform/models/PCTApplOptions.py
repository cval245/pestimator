from django.db import models

from famform.managers import PCTApplOptionsManager
from famform.models.ApplOptions import ApplOptions


class PCTApplOptions(ApplOptions):
    isa_country = models.ForeignKey('characteristics.Country', on_delete=models.CASCADE)

    objects = PCTApplOptionsManager()
