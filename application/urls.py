from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

router = routers.SimpleRouter()
router.register(r'applications', views.ApplicationViewSet, basename='application')
router.register(r'specs', views.ApplDetailViewSet, basename='appldetail')

urlpatterns = router.urls
urlpatterns = format_suffix_patterns(urlpatterns)
