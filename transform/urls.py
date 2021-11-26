from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

from rest_framework import routers


class OptionalSlashRouter(routers.SimpleRouter):
    def __init__(self):
        super().__init__()
        self.trailing_slash = '/?'


router = OptionalSlashRouter()
router.register(r'trans-complex-time',
                views.TransComplexTimeViewSet, basename='transcomplextime')

router.register(r'custom-filing-transform',
                views.CustomFilingTransformViewSet, basename='customfilingtransform')

router.register(r'publication-transform',
                views.PublicationTransformViewSet, basename='publicationtransform')

router.register(r'request-examination-transform',
                views.RequestExaminationTransformViewSet, basename='requestexaminationtransform')

router.register(r'oa-transform',
                views.OATransformViewSet, basename='oatransform')

router.register(r'us-oa-transform',
                views.USOATransformViewSet, basename='usoatransform')

router.register(r'allowance-transform',
                views.AllowanceTransformViewSet, basename='allowancetransform')

router.register(r'issue-transform',
                views.IssueTransformViewSet, basename='issuetransform')

router.register(r'country-oanum',
                views.CountryOANumViewSet, basename='countryoanum')

func_urls = [
    path(r'get-filing-transform-requirements', views.get_needed, name='get_needed')
]

urlpatterns = router.urls + func_urls
urlpatterns = format_suffix_patterns(urlpatterns)
