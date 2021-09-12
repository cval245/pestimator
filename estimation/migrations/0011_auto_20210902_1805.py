# Generated by Django 3.2.3 on 2021-09-02 18:05

from django.db import migrations
import relativedeltafield.fields


class Migration(migrations.Migration):
    dependencies = [
        ('estimation', '0010_auto_20210901_2208'),
    ]

    operations = [
        migrations.AddField(
            model_name='translationesttemplate',
            name='date_diff',
            field=relativedeltafield.fields.RelativeDeltaField(default='P0D'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='TranslationEst',
        ),
    ]