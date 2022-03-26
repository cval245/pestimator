from rest_framework import serializers
from rest_framework.utils.serializer_helpers import ReturnDict

from articles.models import Article


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('id', 'title', 'content', 'date_created', 'slug', 'image_location')


class ArticleBulkSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=255)
    date_created = serializers.DateField()
    content_short = serializers.CharField()
    image_location = serializers.CharField()
    slug = serializers.CharField(max_length=255)

    # @property
    # def data(self):
    #     ret = super().data
    #     ret.content_short = 'lol'
    #     return ReturnDict(ret, serializer=self)
