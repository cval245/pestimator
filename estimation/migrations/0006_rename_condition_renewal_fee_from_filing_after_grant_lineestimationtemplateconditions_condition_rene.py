# Generated by Django 4.0.2 on 2022-02-21 21:21

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('estimation', '0005_alter_allowanceesttemplate_appl_type_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lineestimationtemplateconditions',
            old_name='condition_renewal_fee_from_filing_after_grant',
            new_name='condition_renewal_fee_from_filing_of_prior_after_grant',
        ),
    ]