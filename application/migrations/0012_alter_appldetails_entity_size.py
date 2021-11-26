# Generated by Django 3.2.3 on 2021-10-26 01:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('characteristics', '0009_country_entity_size_available'),
        ('application', '0011_pctapplication_isa_country'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appldetails',
            name='entity_size',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE,
                                    to='characteristics.entitysize'),
        ),
    ]
