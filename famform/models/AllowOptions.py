from famform.managers import AllowOptionsManager
from famform.models.BaseOptions import BaseOptions


class AllowOptions(BaseOptions):
    objects = AllowOptionsManager()

    class Meta:
        abstract = False
