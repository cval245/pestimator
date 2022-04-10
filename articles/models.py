from django.db import models


class Article(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    date_created = models.DateField(auto_now_add=True)
    image_location = models.ImageField(upload_to='article')
    visible = models.BooleanField(default=False)
    content = models.TextField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['slug'],
                name='uniqueSlugArticle'),
            models.UniqueConstraint(
                fields=['title'],
                name='uniqueTitleArticle'),
        ]


# class ArticleParagraph(models.Model):
#     article = models.ForeignKey('Article', on_delete=models.CASCADE)
#     title = models.CharField(max_length=255)
#     content = models.TextField()


class ArticleImage(models.Model):
    article = models.ForeignKey('Article', on_delete=models.CASCADE)
    # image_position = models.ForeignKey('ArticleImagePosition', on_delete=models.PROTECT)
    image_location = models.ImageField(upload_to='article')
    # image_description = models.TextField()

# class ArticleImagePosition(models.Model):
#     name = models.CharField(max_length=255)
