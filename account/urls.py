from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from django.views.decorators.csrf import csrf_exempt
from account import views
from rest_framework import routers


class OptionalSlashRouter(routers.SimpleRouter):
    def __init__(self):
        super().__init__()
        self.trailing_slash = '/?'


router = OptionalSlashRouter()
router.register(r'account/?', views.UserProfileViewSet, basename='account')
router.register(r'account-admin/?', views.UserProfileAdminViewSet, basename='account-admin')
b = [path(r'retrieve-username/', csrf_exempt(views.retrieveUsername))]
c = [path(r'checkout/', csrf_exempt(views.create_checkout_session))]
d = [path(r'webhooks/', csrf_exempt(views.webhook_stripe_add_estimate))]
urlpatterns = router.urls + b + c + d
