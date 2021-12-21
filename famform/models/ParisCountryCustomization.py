from django.db import models



class ParisCountryCustomization(models.Model):
    fam_est_form_data = models.ForeignKey('FamEstFormData', on_delete=models.CASCADE)
    country = models.ForeignKey('characteristics.Country', on_delete=models.CASCADE)
    custom_appl_details = models.OneToOneField('CustomApplDetails',
                                               null=True,
                                               default=None,
                                               on_delete=models.CASCADE)
    custom_appl_options = models.OneToOneField('CustomApplOptions',
                                               null=True,
                                               default=None,
                                               on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['fam_est_form_data', 'country'],
                name='ParisFamEstFormDataCountryUniqueConstraint'),
        ]
