# Generated by Django 3.2.3 on 2021-09-15 21:07

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('estimation', '0018_auto_20210913_2038'),
    ]

    operations = [
        migrations.AddField(
            model_name='baseest',
            name='description',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='baseest',
            name='fee_code',
            field=models.CharField(default=1, max_length=30),
            preserve_default=False,
        ),
    ]