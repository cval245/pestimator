# Generated by Django 4.0.2 on 2022-03-18 00:19

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('lawfirm', '0009_lawfirm_image_location'),
    ]

    operations = [
        migrations.CreateModel(
            name='LawFirmImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(max_length=255)),
            ],
        ),
        migrations.RemoveField(
            model_name='lawfirm',
            name='image_location',
        ),
    ]
