from django.db import models

from famform.managers import USOAOptionsManager
from famform.models.OAOptions import OAOptions


class USOAOptions(OAOptions):
    oa_final_bool = models.BooleanField(default=False)

    objects = USOAOptionsManager()
