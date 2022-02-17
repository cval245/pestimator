from django.urls import path
from django.views.decorators.csrf import csrf_exempt
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
router.register(r'languages', views.LanguageViewSet, basename='languages')
router.register(r'doc-formats', views.DocFormatViewSet, basename='docformat')
router.register(r'doc-formats-countries', views.DocFormatCountryViewSet, basename='docformatcountry')
router.register(r'epvalidation-translation-required',
                views.EPValidationTranslationRequiredViewSet,
                basename='epvalidationtranslationrequired')
router.register(r'translation-required-options',
                views.TranslationRequiredOptionsViewSet,
                basename='translationrequiredoptions')

b = [
    path(r'entity-size/', views.getEntitySize, name='entity-size'),
    path(r'currency/', views.getCurrencyView, name='currency'),
]
urlpatterns = router.urls + b
urlpatterns = format_suffix_patterns(urlpatterns)
