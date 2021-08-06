# Generated by Django 3.2.5 on 2021-08-04 06:48

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('famform', '0002_initial'),
        ('characteristics', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('application', '0003_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='famestformdata',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='apploptions',
            name='appl_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='characteristics.appltype'),
        ),
        migrations.AddField(
            model_name='apploptions',
            name='country',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='characteristics.country'),
        ),
        migrations.AddField(
            model_name='apploptions',
            name='details',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='application.appldetails'),
        ),
        migrations.AddField(
            model_name='apploptions',
            name='fam_options',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='famform.famoptions'),
        ),
        migrations.AddField(
            model_name='apploptions',
            name='prev_appl_options',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='famform.apploptions'),
        ),
        migrations.AddField(
            model_name='allowoptions',
            name='appl',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='famform.apploptions'),
        ),
    ]
