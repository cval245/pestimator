# Generated by Django 4.0.2 on 2022-02-23 22:48

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('estimation',
         '0006_rename_condition_renewal_fee_from_filing_after_grant_lineestimationtemplateconditions_condition_rene'),
    ]

    operations = [
        migrations.AddField(
            model_name='lineestimationtemplateconditions',
            name='condition_renewal_fee_from_filing_after_grant',
            field=models.BooleanField(default=False),
        ),
    ]
