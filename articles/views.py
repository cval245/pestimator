import os

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.models.functions import Substr
from django.utils.text import slugify
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework import permissions, renderers, status
from rest_framework import viewsets
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from articles.models import Article, ArticleImage, ArticleImagePosition
from articles.serializers import ArticleBulkSerializer, ArticleImagePositionSerializer, ArticleImageSerializer, \
    ArticleSerializer
from user.accesspolicies import AllGetStaffOnlyPost, GetOnlyPolicy, StaffOnlyAccess


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

    def get_serializer_class(self):
        slug = self.request.query_params.get('titleslug')
        if self.request.method == 'PUT':
            return ArticleSerializer
        if slug is not None:
            return ArticleSerializer
        else:
            return ArticleBulkSerializer

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
            queryset = Article.objects.filter(slug=slug, visible=True).prefetch_related('articleimage_set')
        else:
            queryset = Article.objects.filter(visible=True).annotate(content_short=Substr('content', 1, 255)).order_by(
                '-date_created')
        return queryset

    def get_serializer_class(self):
        slug = self.request.query_params.get('titleslug')
        if slug is not None:
            return ArticleSerializer
        else:
            return ArticleBulkSerializer

    def list(self, request, **kwargs):
        slug = self.request.query_params.get('titleslug')
        if slug is not None:
            if Article.objects.filter(slug=slug).exists() is False:
                return Response(status=status.HTTP_404_NOT_FOUND)
        return super().list(request)


class ImageArticleViewSet(viewsets.ModelViewSet):
    serializer_class = ArticleImageSerializer
    permission_classes = [AllGetStaffOnlyPost]

    def get_queryset(self):
        article_id = self.request.query_params.get('articleid')
        if article_id is not None:
            queryset = ArticleImage.objects.filter(article=article_id)
        else:
            queryset = ArticleImage.objects.all()
        return queryset


class ArticleImagePositionViewSet(viewsets.ModelViewSet):
    serializer_class = ArticleImagePositionSerializer
    permission_classes = [AllGetStaffOnlyPost]

    def get_queryset(self):
        return ArticleImagePosition.objects.all()


class WebpRenderer(renderers.BaseRenderer):
    media_type = 'image/webp'
    format = 'webp'
    charset = None
    render_style = 'binary'

    def render(self, data, media_type=None, accepted_media_type='image/webp', renderer_context=None):
        return data


@api_view(['POST'])
@renderer_classes([WebpRenderer])
@permission_classes([AllGetStaffOnlyPost])
def post_article_image(request, article_id):
    image = request.data['file']
    if Article.objects.filter(id=article_id).exists():
        article = Article.objects.get(id=article_id)
        if article.image_location:
            old_save_name = article.image_location.path
            if os.path.exists(old_save_name):
                os.remove(old_save_name)
        article.image_location = image
        article.save()
        return Response(image)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@renderer_classes([WebpRenderer])
@permission_classes([AllGetStaffOnlyPost])
def post_article_image_image_post(request, article_image_id):
    image = request.data['file']
    if ArticleImage.objects.filter(id=article_image_id).exists():
        article_image = ArticleImage.objects.get(id=article_image_id)
        article_image.image_location = image
        if isinstance(image, InMemoryUploadedFile):
            article_image.save()
        serializer = ArticleImageSerializer(article_image)
        json = JSONRenderer().render(serializer.data)
        return Response(json)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)
