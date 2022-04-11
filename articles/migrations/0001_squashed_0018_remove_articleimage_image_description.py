# Generated by Django 4.0.2 on 2022-04-11 07:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    replaces = [('articles', '0001_initial'), ('articles', '0002_article_slug'),
                ('articles', '0003_article_image_location'), ('articles', '0004_article_visible'),
                ('articles', '0005_article_uniqueslugarticle_article_uniquetitlearticle'),
                ('articles', '0006_alter_article_image_location'), ('articles', '0007_alter_article_image_location'),
                ('articles', '0008_articleimages'), ('articles', '0009_article_images'),
                ('articles', '0010_rename_articleimages_articleimage'),
                ('articles', '0011_rename_image_style_articleimage_image_position_and_more'),
                ('articles', '0012_articleimageposition_and_more'), ('articles', '0013_articleimage_image_description'),
                ('articles', '0014_remove_article_content_remove_articleimage_article_and_more'),
                ('articles', '0015_articleimage_paragraph'),
                ('articles', '0016_remove_articleparagraph_article_and_more'), ('articles', '0017_article_content'),
                ('articles', '0018_remove_articleimage_image_description')]

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('content', models.TextField()),
                ('date_created', models.DateField(auto_now_add=True)),
                ('slug', models.SlugField(default=1, max_length=255)),
                ('image_location', models.CharField(default=1, max_length=255)),
                ('visible', models.BooleanField(default=False)),
            ],
        ),
        migrations.AddConstraint(
            model_name='article',
            constraint=models.UniqueConstraint(fields=('slug',), name='uniqueSlugArticle'),
        ),
        migrations.AddConstraint(
            model_name='article',
            constraint=models.UniqueConstraint(fields=('title',), name='uniqueTitleArticle'),
        ),
        migrations.AlterField(
            model_name='article',
            name='image_location',
            field=models.CharField(default='default', max_length=255),
        ),
        migrations.AlterField(
            model_name='article',
            name='image_location',
            field=models.ImageField(upload_to='article'),
        ),
        migrations.RemoveField(
            model_name='article',
            name='content',
        ),
        migrations.AddField(
            model_name='article',
            name='content',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='ArticleImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_location', models.ImageField(upload_to='article')),
                ('article',
                 models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='articles.article')),
            ],
        ),
    ]
