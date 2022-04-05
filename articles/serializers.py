from rest_framework import serializers
from articles.models import Article, ArticleImage, ArticleImagePosition


class ArticleImagePositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleImagePosition
        fields = ('id', 'name')


class ArticleImageSerializer(serializers.ModelSerializer):
    image_location = serializers.ImageField(read_only=True, use_url=True)
    image_position = serializers.PrimaryKeyRelatedField(queryset=ArticleImagePosition.objects.all())

    class Meta:
        model = ArticleImage
        fields = ('id', 'image_position', 'image_location', 'article')


class ArticleSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField()
    date_created = serializers.DateField(read_only=True)
    image_location = serializers.ImageField(read_only=True, use_url=True)
    articleimage_set = ArticleImageSerializer(many=True, read_only=True)

    class Meta:
        model = Article
        fields = ('id', 'title', 'content', 'date_created', 'articleimage_set',
                  'slug', 'image_location', 'visible')


class ArticleBulkSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=255)
    date_created = serializers.DateField(read_only=True)
    content_short = serializers.CharField(read_only=True)
    image_location = serializers.ImageField(read_only=True, use_url=True)
    visible = serializers.BooleanField()
    slug = serializers.CharField(max_length=255)
