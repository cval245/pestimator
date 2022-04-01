from rest_framework import routers

from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views


class OptionalSlashRouter(routers.SimpleRouter):
    def __init__(self):
        super().__init__()
        self.trailing_slash = '/?'


router = OptionalSlashRouter()
router.register(r'article', views.ArticleViewSet,
                basename='article')
router.register(r'article-full', views.ArticleAdminViewSet,
                basename='article-full')

urlpatterns = router.urls
b = [
    path(r'get-article-image/<str:image_location>', views.get_article_image, name='getarticleimage'),
    path(r'post-article-image/<int:article_id>', views.post_article_image, name='postarticleimage')
]
urlpatterns += b
urlpatterns = format_suffix_patterns(urlpatterns)
