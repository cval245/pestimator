from django.db import models


class EPMethodCustomization(models.Model):
    custom_appl_details = models.OneToOneField('CustomApplDetails',
                                               null=True,
                                               default=None,
                                               on_delete=models.CASCADE)
    custom_appl_options = models.OneToOneField('CustomApplOptions',
                                               null=True,
                                               default=None,
                                               on_delete=models.CASCADE)
