# Generated by Django 3.2.3 on 2021-11-30 04:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('characteristics', '0019_auto_20211129_1749'),
        ('estimation', '0035_auto_20211129_1739'),
    ]

    operations = [
        migrations.AddField(
            model_name='lineestimationtemplateconditions',
            name='language',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE,
                                    to='characteristics.language'),
        ),
    ]
