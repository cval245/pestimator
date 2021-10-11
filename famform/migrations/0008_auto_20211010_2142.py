# Generated by Django 3.2.5 on 2021-10-10 21:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('characteristics', '0004_country_available_appl_types'),
        ('famform', '0007_auto_20211009_0444'),
    ]

    operations = [
        migrations.AddField(
            model_name='famestformdata',
            name='isa_country',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='isa_country',
                                    to='characteristics.country'),
        ),
        migrations.CreateModel(
            name='PCTApplOptions',
            fields=[
                ('apploptions_ptr',
                 models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True,
                                      primary_key=True, serialize=False, to='famform.apploptions')),
                ('isa_country',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='characteristics.country')),
            ],
            bases=('famform.apploptions',),
        ),
    ]
