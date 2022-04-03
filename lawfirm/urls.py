from rest_framework import routers

from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views


class OptionalSlashRouter(routers.SimpleRouter):
    def __init__(self):
        super().__init__()
        self.trailing_slash = '/?'


router = OptionalSlashRouter()
router.register(r'law-firms', views.LawFirmViewSet,
                basename='law-firms')
router.register(r'law-firms-full', views.LawFirmAdminViewSet,
                basename='law-firms-full')

urlpatterns = router.urls
b = [
    path(r'post-law-firm-image/<int:lawfirm_id>', views.post_lawfirm_image, name='postlawfirmimage'),
]
urlpatterns += b
urlpatterns = format_suffix_patterns(urlpatterns)
