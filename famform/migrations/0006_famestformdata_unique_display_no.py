# Generated by Django 3.2.5 on 2021-10-07 05:11

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('famform', '0005_apploptions_translation_full_required'),
    ]

    operations = [
        migrations.AddField(
            model_name='famestformdata',
            name='unique_display_no',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
