from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'families', views.FamilyViewSet, basename='family')

func_urls = [
	path(r'fam-est/', views.fam_est_all, name='fam-est-all'),
    path(r'fam-est-detail/<int:id>', views.fam_est, name='fam-est'),
    path(r'fam-est-detail/', views.fam_est_detail, name='fam-est-detail')
]


urlpatterns = router.urls + func_urls
urlpatterns = format_suffix_patterns(urlpatterns)
