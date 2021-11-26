from django.db import models

from characteristics.models import EntitySize, Languages


class CustomApplDetails(models.Model):
    num_indep_claims = models.IntegerField(default=None, null=True)
    num_claims = models.IntegerField(default=None, null=True)
    num_claims_multiple_dependent = models.IntegerField(default=None, null=True)
    num_drawings = models.IntegerField(default=None, null=True)
    num_pages_description = models.IntegerField(default=None, null=True)
    num_pages_claims = models.IntegerField(default=None, null=True)
    num_pages_drawings = models.IntegerField(default=None, null=True)
    entity_size = models.ForeignKey(EntitySize, on_delete=models.CASCADE,
                                    default=None, null=True)
    language = models.ForeignKey(Languages, on_delete=models.CASCADE,
                                 default=None, null=True)
