# Generated by Django 3.2.3 on 2021-11-19 15:16

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('estimation', '0027_auto_20211119_1437'),
    ]

    operations = [
        migrations.AddField(
            model_name='lineestimationtemplateconditions',
            name='condition_claims_multiple_dependent_max',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='lineestimationtemplateconditions',
            name='condition_claims_multiple_dependent_min',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
