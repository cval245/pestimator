# Generated by Django 4.0.2 on 2022-03-17 23:56

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('lawfirm', '0008_lawfirm_slug_alter_lawfirm_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='lawfirm',
            name='image_location',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]