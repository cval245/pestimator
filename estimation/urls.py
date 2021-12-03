from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

from . import views


class OptionalSlashRouter(routers.SimpleRouter):
    def __init__(self):
        super().__init__()
        self.trailing_slash = '/?'


router = OptionalSlashRouter()
router.register(r'base-est-template', views.BaseEstTemplateViewSet,
                basename='baseesttemplate')
router.register(r'filing-est-template',
                views.FilingEstimateTemplateViewSet, basename='filingesttemplate')
router.register(r'publication-est-template',
                views.PublicationEstTemplateViewSet, basename='filingesttemplate')
router.register(r'request-exam-est-template',
                views.RequestExamEstTemplateViewSet, basename='requestexamesttemplate')
router.register(r'oa-est-template',
                views.OAEstimateTemplateViewSet, basename='oaestimatetemplate')
router.register(r'us-oa-est-template',
                views.USOAEstimateTemplateViewSet, basename='usoaestimatetemplate')
router.register(r'allowance-est-template',
                views.AllowanceEstTemplateViewSet, basename='allowanceestimatetemplate')
router.register(r'issue-est-template',
                views.IssueEstTemplateViewSet, basename='issueestimatetemplate')
router.register(r'lawfirm-est-template',
                views.LawFirmEstTemplateViewSet, basename='lawfirmestimatetemplate')
router.register(r'conditions',
                views.ConditionsViewSet, basename='conditionsviewset')
router.register(r'complex-conditions',
                views.ComplexConditionsViewSet, basename='complexconditionsviewset')
router.register(r'complex-time-conditions',
                views.ComplexTimeConditionsViewSet, basename='complextimeconditionsviewset')
router.register(r'fee-category',
                views.FeeCategoryViewSet, basename='feecategoryviewset')

urlpatterns = router.urls
urlpatterns = format_suffix_patterns(urlpatterns)
