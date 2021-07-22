# Generated by Django 3.2.5 on 2021-07-21 21:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('characteristics', '0002_appltype_applicationtypeuniqueconstraint'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='entitysize',
            constraint=models.UniqueConstraint(fields=('entity_size',), name='entitySizeUniqueConstraint'),
        ),
        migrations.AddConstraint(
            model_name='oanumpercountry',
            constraint=models.UniqueConstraint(fields=('country',), name='countryOANumUniqueConstraint'),
        ),
    ]
