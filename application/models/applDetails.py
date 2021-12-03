from django.db import models

from characteristics.models import EntitySize, Language


class ApplDetails(models.Model):
    num_indep_claims = models.IntegerField()
    num_claims = models.IntegerField()
    num_claims_multiple_dependent = models.IntegerField()
    num_drawings = models.IntegerField()
    num_pages_description = models.IntegerField()
    num_pages_claims = models.IntegerField()
    num_pages_drawings = models.IntegerField()
    entity_size = models.ForeignKey(EntitySize, on_delete=models.CASCADE, null=True)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)

    @property
    def total_pages(self):
        return self.num_pages_claims + self.num_pages_drawings + self.num_pages_description
