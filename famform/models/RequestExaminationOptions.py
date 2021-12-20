from famform.managers import RequestExaminationOptionsManager
from famform.models.BaseOptions import BaseOptions


class RequestExaminationOptions(BaseOptions):
    objects = RequestExaminationOptionsManager()

    class Meta:
        abstract = False
