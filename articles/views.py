from PIL import Image
import uuid as uuid
import os
from django.conf import settings
from django.db.models.functions import Substr
from django.utils.text import slugify
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework import permissions, renderers, status
from rest_framework import viewsets
from rest_framework.response import Response
from articles.models import Article
from articles.serializers import ArticleBulkSerializer, ArticleSerializer
from user.accesspolicies import GetOnlyPolicy, StaffOnlyAccess


class ArticleAdminViewSet(viewsets.ModelViewSet):
    serializer_class = ArticleSerializer
    permission_classes = [StaffOnlyAccess]

    def get_queryset(self):
        slug = self.request.query_params.get('titleslug')
        if slug is not None:
            queryset = Article.objects.filter(slug=slug)
        else:
            queryset = Article.objects.all().annotate(content_short=Substr('content', 1, 255)).order_by('-date_created')
        return queryset

    #
    # def get_serializer(self, *args, **kwargs):
    #     slug = self.request.query_params.get('titleslug')
    #     queryset = self.get_queryset()
    #     if slug is not None:
    #         serializer = ArticleSerializer(queryset, many=True)
    #     else:
    #         serializer = ArticleBulkSerializer(queryset, many=True)
    #     return serializer

    def get_serializer_class(self):
        slug = self.request.query_params.get('titleslug')
        if slug is not None:
            serializer = ArticleSerializer
        else:
            serializer = ArticleBulkSerializer
        return serializer

    def list(self, request, **kwargs):
        slug = self.request.query_params.get('titleslug')
        if slug is not None:
            if Article.objects.filter(slug=slug).exists() is False:
                return Response(status=status.HTTP_404_NOT_FOUND)
        return super().list(request)

    def create(self, request, *args, **kwargs):
        new_request = request
        request.data['slug'] = slugify(request.data['title'])
        context = {'request': new_request}
        serializer = ArticleSerializer(data=request.data, context=context)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        request.data['slug'] = slugify(request.data['title'])
        return super().update(request=request, args=args, kwargs=kwargs)


class ArticleViewSet(viewsets.ModelViewSet):
    serializer_class = ArticleSerializer
    permission_classes = [GetOnlyPolicy]

    def get_queryset(self):
        slug = self.request.query_params.get('titleslug')
        if slug is not None:
            queryset = Article.objects.filter(slug=slug, visible=True)
        else:
            queryset = Article.objects.filter(visible=True).annotate(content_short=Substr('content', 1, 255)).order_by(
                '-date_created')
        return queryset

    def list(self, request, **kwargs):
        slug = self.request.query_params.get('titleslug')
        queryset = self.get_queryset()
        if slug is not None:
            serializer = ArticleSerializer(queryset, many=True)
        else:
            serializer = ArticleBulkSerializer(queryset, many=True)
        return Response(serializer.data)


class WebpRenderer(renderers.BaseRenderer):
    media_type = 'image/webp'
    format = 'webp'
    charset = None
    render_style = 'binary'

    def render(self, data, media_type=None, accepted_media_type='image/webp', renderer_context=None):
        return data


@api_view(['POST'])
@renderer_classes([WebpRenderer])
@permission_classes([permissions.IsAuthenticatedOrReadOnly])
def post_article_image(request, article_id):
    image = request.data['file']
    if Article.objects.filter(id=article_id).exists():
        article = Article.objects.get(id=article_id)
        old_save_name = article.image_location.path
        if os.path.exists(old_save_name):
            os.remove(old_save_name)
        article.image_location = image
        article.save()
        return Response(image)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

