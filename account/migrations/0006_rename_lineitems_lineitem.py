# Generated by Django 3.2.3 on 2021-09-23 20:54

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('account', '0005_auto_20210923_2046'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='LineItems',
            new_name='LineItem',
        ),
    ]
