# Create your models here.
from famform.managers import IssueOptionsManager
from famform.models.BaseOptions import BaseOptions


class IssueOptions(BaseOptions):
    objects = IssueOptionsManager()

    class Meta:
        abstract = False
