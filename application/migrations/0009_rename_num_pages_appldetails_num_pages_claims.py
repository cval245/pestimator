# Generated by Django 3.2.3 on 2021-09-15 03:04

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('application', '0008_appldetails_num_pages_description'),
    ]

    operations = [
        migrations.RenameField(
            model_name='appldetails',
            old_name='num_pages',
            new_name='num_pages_claims',
        ),
    ]