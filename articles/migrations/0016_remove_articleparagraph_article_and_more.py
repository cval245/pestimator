# Generated by Django 4.0.2 on 2022-04-10 17:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('articles', '0015_articleimage_paragraph'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='articleparagraph',
            name='article',
        ),
        migrations.RemoveField(
            model_name='articleimage',
            name='image_position',
        ),
        # migrations.RemoveField(
        #     model_name='articleimage',
        #     name='paragraph',
        # ),
        migrations.AddField(
            model_name='articleimage',
            name='article',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='articles.article'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='ArticleImagePosition',
        ),
        migrations.DeleteModel(
            name='ArticleParagraph',
        ),
    ]
