from django.db import models


# Create your models here.

class Article(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    content = models.TextField()
    date_created = models.DateField(auto_now_add=True)
    image_location = models.CharField(max_length=255, default='default')
    visible = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['slug'],
                name='uniqueSlugArticle'),
            models.UniqueConstraint(
                fields=['title'],
                name='uniqueTitleArticle'),
        ]
