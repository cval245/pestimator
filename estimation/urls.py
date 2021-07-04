from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'base-est-template', views.BaseEstTemplateViewSet, basename='baseesttemplate')
router.register(r'filing-est-template', 
	views.FilingEstimateTemplateViewSet, basename='filingesttemplate')
router.register(r'publication-est-template', 
	views.PublicationEstTemplateViewSet, basename='filingesttemplate')
router.register(r'oa-estimate-template',
	views.OAEstimateTemplateViewSet, basename='oaestimatetemplate')
router.register(r'allowance-estimate-template',
	views.AllowanceEstTemplateViewSet, basename='allowanceestimatetemplate')
router.register(r'issue-estimate-template',
	views.IssueEstTemplateViewSet, basename='issueestimatetemplate')

urlpatterns = router.urls
urlpatterns = format_suffix_patterns(urlpatterns)