from django.db import models
from application.models.baseApplication import BaseApplication
from characteristics.models import Country


class PCTApplication(BaseApplication):
    # normal country variable is the REceiveing office
    # isa_country is the International Search Authority Country
    isa_country = models.ForeignKey(Country, on_delete=models.CASCADE)

    class Meta:
        abstract = False
        # Todo possibly add meta options constraint to ensure isa_country
        # is valid for country.  maybe not due to db compatibility issues
