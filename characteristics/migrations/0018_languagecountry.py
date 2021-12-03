# Generated by Django 3.2.3 on 2021-11-29 17:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('characteristics', '0017_delete_languages'),
    ]

    operations = [
        migrations.CreateModel(
            name='LanguageCountry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('default', models.BooleanField(default=False)),
                ('appl_type',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='characteristics.appltype')),
                ('country',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='characteristics.country')),
                ('language',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='characteristics.language')),
            ],
        ),
    ]
