from django.urls import path
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

from . import views


class OptionalSlashRouter(routers.SimpleRouter):
    def __init__(self):
        super().__init__()
        self.trailing_slash = '/?'


router = OptionalSlashRouter()

router.register(r'appl-types', views.ApplTypeViewSet, basename='applType')
router.register(r'appl-types-all', views.ApplTypeAllViewSet, basename='applType')
router.register(r'countries', views.CountryViewSet, basename='countries')
router.register(r'countries-all', views.CountryAllViewSet, basename='countriesall')

b = [
    path(r'entity-size/', views.getEntitySize, name='entity-size'),
]
urlpatterns = router.urls + b
urlpatterns = format_suffix_patterns(urlpatterns)
