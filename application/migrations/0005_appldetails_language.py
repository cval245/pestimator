# Generated by Django 3.2.3 on 2021-08-31 19:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('characteristics', '0002_languages'),
        ('application', '0004_baseapplication_appl_option'),
    ]

    operations = [
        migrations.AddField(
            model_name='appldetails',
            name='language',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE,
                                    to='characteristics.languages'),
            preserve_default=False,
        ),
    ]
