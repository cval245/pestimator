from django.db import models

from famform.managers import PCTApplOptionsManager
from famform.models.ApplOptions import ApplOptions


class PCTApplOptions(ApplOptions):
    isa_country = models.ForeignKey('characteristics.Country', on_delete=models.CASCADE)
    isa_entity_size = models.ForeignKey('characteristics.EntitySize', on_delete=models.CASCADE, null=True)

    objects = PCTApplOptionsManager()
