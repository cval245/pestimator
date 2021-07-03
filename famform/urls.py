from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'fam-est-form-data', views.FamEstFormDataViewSet,
                basename='fameEstFormData')
urlpatterns = router.urls
urlpatterns = format_suffix_patterns(urlpatterns)