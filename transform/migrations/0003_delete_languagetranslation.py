# Generated by Django 3.2.3 on 2021-09-01 22:08

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('transform', '0002_languagetranslation'),
    ]

    operations = [
        migrations.DeleteModel(
            name='LanguageTranslation',
        ),
    ]
