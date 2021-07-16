from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import include
from . import views

from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'appl-types', views.ApplTypeViewSet)
router.register(r'countries', views.CountryViewSet, basename='countries')
router.register(r'countries-all', views.CountryAllViewSet, basename='countriesall')

b = [
    path(r'entity-size/', views.getEntitySize, name='entity-size'),
]
urlpatterns = router.urls + b
urlpatterns = format_suffix_patterns(urlpatterns)
