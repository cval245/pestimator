from rest_framework import serializers
from articles.models import Article


class ArticleSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField()
    date_created = serializers.DateField(read_only=True)
    image_location = serializers.ImageField(read_only=True, use_url=True)

    class Meta:
        model = Article
        fields = ('id', 'title', 'content', 'date_created',
                  'slug', 'image_location', 'visible')


class ArticleBulkSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=255)
    date_created = serializers.DateField(read_only=True)
    content_short = serializers.CharField()
    image_location = serializers.ImageField(read_only=True, use_url=True)
    visible = serializers.BooleanField()
    slug = serializers.CharField(max_length=255)
