# Generated by Django 3.2.3 on 2021-12-02 22:43

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('famform', '0044_apploptions_translation_implemented'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='apploptions',
            name='translation_full_required',
        ),
    ]
