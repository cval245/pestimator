# Generated by Django 3.2.3 on 2021-09-02 22:03

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('application', '0005_appldetails_language'),
    ]

    operations = [
        migrations.AddField(
            model_name='appldetails',
            name='num_pages_drawings',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
