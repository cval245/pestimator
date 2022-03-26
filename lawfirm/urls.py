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

urlpatterns = router.urls
b = [
    path(r'get-law-firm-image/<str:image_location>', views.get_law_firm_image, name='getlawfirmimage')
]
urlpatterns += b
urlpatterns = format_suffix_patterns(urlpatterns)
