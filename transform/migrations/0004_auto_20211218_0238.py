# Generated by Django 3.2.9 on 2021-12-18 02:38

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('transform', '0003_auto_20211216_2146'),
    ]

    operations = [
        migrations.RenameField(
            model_name='allowancetransform',
            old_name='complex_time_conditions',
            new_name='trans_complex_time_condition',
        ),
        migrations.RenameField(
            model_name='customfilingtransform',
            old_name='complex_time_conditions',
            new_name='trans_complex_time_condition',
        ),
        migrations.RenameField(
            model_name='issuetransform',
            old_name='complex_time_conditions',
            new_name='trans_complex_time_condition',
        ),
        migrations.RenameField(
            model_name='oatransform',
            old_name='complex_time_conditions',
            new_name='trans_complex_time_condition',
        ),
        migrations.RenameField(
            model_name='publicationtransform',
            old_name='complex_time_conditions',
            new_name='trans_complex_time_condition',
        ),
        migrations.RenameField(
            model_name='requestexaminationtransform',
            old_name='complex_time_conditions',
            new_name='trans_complex_time_condition',
        ),
    ]
