from django.db import models

from characteristics.models import Country
from famform.models.ApplOptions import ApplOptions


class PCTApplOptions(ApplOptions):
    isa_country = models.ForeignKey(Country, on_delete=models.CASCADE)
