# Generated by Django 3.2.9 on 2021-12-16 21:46

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('transform', '0002_auto_20211216_2137'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='allowancetransform',
            name='AllowanceCountryUniqueConstraint',
        ),
        migrations.RemoveConstraint(
            model_name='issuetransform',
            name='IssueCountryUniqueConstraint',
        ),
        migrations.RemoveConstraint(
            model_name='publicationtransform',
            name='PublicationCountryUniqueConstraint',
        ),
        migrations.AddConstraint(
            model_name='allowancetransform',
            constraint=models.UniqueConstraint(fields=('country', 'appl_type'),
                                               name='AllowanceCountryApplTypeUniqueConstraint'),
        ),
        migrations.AddConstraint(
            model_name='issuetransform',
            constraint=models.UniqueConstraint(fields=('country', 'appl_type'),
                                               name='IssueCountryApplTypeUniqueConstraint'),
        ),
        migrations.AddConstraint(
            model_name='publicationtransform',
            constraint=models.UniqueConstraint(fields=('country', 'appl_type'),
                                               name='PublicationCountryApplTypeUniqueConstraint'),
        ),
    ]
