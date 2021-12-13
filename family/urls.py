from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'families', views.FamilyViewSet, basename='family')
router.register(r'families-all', views.FamilyAllViewSet, basename='family-all')

func_urls = [
    path(r'fam-est/', views.fam_est_all, name='fam-est-all'),
    path(r'fam-est-specific-user/', views.fam_est_all_specific_user, name='fam-est-all-specific-user'),
    path(r'fam-est-det-tot/', views.fam_est_get_tot_costs, name='fam-est-det-tot'),
    # path(r'fam-est-detail/<int:id>', views.fam_est, name='fam-est'),
    path(r'fam-est-detail/', views.fam_est_detail, name='fam-est-detail'),
    path(r'get-excel-report/', views.get_excel_report_fam_est_detail, name='get-excel-report'),
    path(r'get-pdf-report/', views.get_pdf_report_fam_est_detail, name='get-pdf-report')
]


urlpatterns = router.urls + func_urls
urlpatterns = format_suffix_patterns(urlpatterns)
