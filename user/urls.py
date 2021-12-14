from rest_framework import routers
from user import views

# router = routers.SimpleRouter()
class OptionalSlashRouter(routers.SimpleRouter):
    def __init__(self):
        super().__init__()
        self.trailing_slash = '/?'


router = OptionalSlashRouter()

router.register(r'user-detail', views.UserViewSet, basename='user')
router.register(r'user-all', views.UserAllViewSet, basename='user-all')
urlpatterns = router.urls
