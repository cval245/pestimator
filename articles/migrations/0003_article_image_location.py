# Generated by Django 4.0.2 on 2022-03-21 06:28

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('articles', '0002_article_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='image_location',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]
