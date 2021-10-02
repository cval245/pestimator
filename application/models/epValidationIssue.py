from django.db import models

from application.models import BaseIssue, EPValidationApplication


class EPValidationIssue(BaseIssue):
    application = models.OneToOneField(
        EPValidationApplication, on_delete=models.CASCADE,
    )

    class Meta:
        abstract = False
