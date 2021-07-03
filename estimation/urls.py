from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

from rest_framework import routers

router = routers.SimpleRouter()

urlpatterns = router.urls
urlpatterns = format_suffix_patterns(urlpatterns)