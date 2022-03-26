from os.path import exists

from django.conf import settings
from django.db.models.functions import Substr
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework import permissions, renderers, viewsets
from rest_framework import viewsets
from rest_framework.response import Response
from articles.models import Article
from articles.serializers import ArticleBulkSerializer, ArticleSerializer
from user.accesspolicies import GetOnlyPolicy


class ArticleViewSet(viewsets.ModelViewSet):
    serializer_class = ArticleSerializer
    permission_classes = [GetOnlyPolicy]

    def get_queryset(self):
        queryset = Article.objects.all()
        slug = self.request.query_params.get('titleslug')
        if slug is not None:
            queryset = Article.objects.filter(slug=slug)

        return queryset

    def list(self, request):
        queryset = Article.objects.all().annotate(content_short=Substr('content', 1, 255))
        slug = self.request.query_params.get('titleslug')
        if slug is not None:
            queryset = Article.objects.filter(slug=slug)
            serializer = ArticleSerializer(queryset, many=True)

        else:
            queryset = Article.objects.all().annotate(content_short=Substr('content', 1, 255))
            serializer = ArticleBulkSerializer(queryset, many=True)
        return Response(serializer.data)


class WebpRenderer(renderers.BaseRenderer):
    media_type = 'image/webp'
    format = 'webp'
    charset = None
    render_style = 'binary'

    def render(self, data, media_type=None, renderer_context=None):
        return data


@api_view(['GET'])
@renderer_classes([WebpRenderer])
@permission_classes([permissions.IsAuthenticatedOrReadOnly])
def get_article_image(request, image_location):
    try:
        image = open(settings.STATIC_ROOT + '/article/' + image_location + '.webp', "br")
    except FileNotFoundError:
        image = open(settings.STATIC_ROOT + '/article/empty.webp', 'br')
    return Response(image)
