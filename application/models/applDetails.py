from django.db import models

from characteristics.models import EntitySize


class ApplDetails(models.Model):
    num_indep_claims = models.IntegerField()
    num_pages = models.IntegerField()
    num_claims = models.IntegerField()
    num_drawings = models.IntegerField()
    entity_size = models.ForeignKey(EntitySize, on_delete=models.CASCADE)