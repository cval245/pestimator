# Generated by Django 3.2.5 on 2021-10-09 04:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('characteristics', '0004_country_available_appl_types'),
        ('famform', '0006_famestformdata_unique_display_no'),
    ]

    operations = [
        migrations.RenameField(
            model_name='famestformdata',
            old_name='method',
            new_name='pct_method',
        ),
        migrations.RemoveField(
            model_name='famestformdata',
            name='countries',
        ),
        migrations.RemoveField(
            model_name='famestformdata',
            name='meth_country',
        ),
        migrations.AddField(
            model_name='famestformdata',
            name='ep_countries',
            field=models.ManyToManyField(related_name='ep_countries', to='characteristics.Country'),
        ),
        migrations.AddField(
            model_name='famestformdata',
            name='paris_countries',
            field=models.ManyToManyField(related_name='paris_countries', to='characteristics.Country'),
        ),
        migrations.AddField(
            model_name='famestformdata',
            name='pct_countries',
            field=models.ManyToManyField(related_name='pct_countries', to='characteristics.Country'),
        ),
        migrations.AddField(
            model_name='famestformdata',
            name='pct_country',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pct_country',
                                    to='characteristics.country'),
        ),
    ]
