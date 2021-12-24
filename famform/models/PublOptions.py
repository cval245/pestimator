from famform.managers import BaseOptionsManager, PublOptionsManager
from famform.models.BaseOptions import BaseOptions


class PublOptions(BaseOptions):
    objects = PublOptionsManager()

    class Meta:
        abstract = False
