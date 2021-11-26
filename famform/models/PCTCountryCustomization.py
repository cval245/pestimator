from django.db import models

from characteristics.models import Country
from famform.models.CustomApplDetails import CustomApplDetails
from famform.models.CustomApplOptions import CustomApplOptions
from famform.models.FamEstFormData import FamEstFormData


class PCTCountryCustomization(models.Model):
    fam_est_form_data = models.ForeignKey(FamEstFormData, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    custom_appl_details = models.OneToOneField(CustomApplDetails,
                                               null=True,
                                               default=None,
                                               on_delete=models.CASCADE)
    custom_appl_options = models.OneToOneField(CustomApplOptions,
                                               null=True,
                                               default=None,
                                               on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['fam_est_form_data', 'country'],
                name='PCTFamEstFormDataCountryUniqueConstraint'),
        ]
