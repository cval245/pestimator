# Generated by Django 3.2.3 on 2021-11-13 06:09

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('estimation', '0022_auto_20211022_0433'),
    ]

    operations = [
        migrations.AddField(
            model_name='lineestimationtemplateconditions',
            name='condition_annual_prosecution_fee_until_grant',
            field=models.BooleanField(default=False),
        ),
    ]
