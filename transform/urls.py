from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'custom-filing-transform', 
	views.CustomFilingTransformViewSet, basename='customfilingtransform')

router.register(r'publication-transform', 
	views.PublicationTransformViewSet, basename='publicationtransform')

router.register(r'oa-transform', 
	views.OATransformViewSet, basename='oatransform')

router.register(r'allowance-transform', 
	views.AllowanceTransformViewSet, basename='allowancetransform')

router.register(r'issue-transform', 
	views.IssueTransformViewSet, basename='issuetransform')

router.register(r'country-oanum', 
	views.CountryOANumViewSet, basename='countryoanum')

urlpatterns = router.urls
urlpatterns = format_suffix_patterns(urlpatterns)