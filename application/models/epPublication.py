from django.db import models

from application.models import EPApplication


class EPPublication(models.Model):
    date_publication = models.DateField()
    application = models.OneToOneField(
        EPApplication, on_delete=models.CASCADE,
    )

    class Meta:
        abstract = False