# Generated by Django 3.2.5 on 2021-10-13 07:00

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('characteristics', '0005_country_isa_countries'),
    ]

    operations = [
        migrations.RenameField(
            model_name='country',
            old_name='pct_analysis_bool',
            new_name='pct_accept_bool',
        ),
        migrations.AddField(
            model_name='country',
            name='pct_ro_bool',
            field=models.BooleanField(default=False),
        ),
    ]
