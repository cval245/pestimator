# Generated by Django 3.2.3 on 2021-10-23 02:51

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('characteristics', '0008_country_ep_validation_translation_required'),
        ('famform', '0009_auto_20211023_0249'),
    ]

    operations = [
        # migrations.AlterField(
        #     model_name='famestformdata',
        #     name='ep_countries',
        #     field=models.ManyToManyField(related_name='ep_countries', through='famform.EPCountryCustomization', to='characteristics.Country'),
        # ),
        # migrations.AlterField(
        #     model_name='famestformdata',
        #     name='paris_countries',
        #     field=models.ManyToManyField(related_name='paris_countries', through='famform.ParisCountryCustomization', to='characteristics.Country'),
        # ),
        # migrations.AlterField(
        #     model_name='famestformdata',
        #     name='pct_countries',
        #     field=models.ManyToManyField(related_name='pct_countries', through='famform.PCTCountryCustomization', to='characteristics.Country'),
        # ),
    ]
