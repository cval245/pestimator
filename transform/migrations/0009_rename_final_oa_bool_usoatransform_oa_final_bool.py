# Generated by Django 4.0.1 on 2022-01-20 06:38

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('transform', '0008_requestexaminationtransform_requestexaminationcountryappltypeuniqueconstraint'),
    ]

    operations = [
        migrations.RenameField(
            model_name='usoatransform',
            old_name='final_oa_bool',
            new_name='oa_final_bool',
        ),
    ]