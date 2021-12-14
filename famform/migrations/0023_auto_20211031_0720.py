# Generated by Django 3.2.3 on 2021-10-31 07:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [

        ('application', '0012_alter_appldetails_entity_size'),
        ('famform', '0022_auto_20211023_2258'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='famestformdata',
            name='entity_size',
        ),
        migrations.RemoveField(
            model_name='famestformdata',
            name='init_appl_claims',
        ),
        migrations.RemoveField(
            model_name='famestformdata',
            name='init_appl_drawings',
        ),
        migrations.RemoveField(
            model_name='famestformdata',
            name='init_appl_indep_claims',
        ),
        migrations.RemoveField(
            model_name='famestformdata',
            name='init_appl_pages_claims',
        ),
        migrations.RemoveField(
            model_name='famestformdata',
            name='init_appl_pages_desc',
        ),
        migrations.RemoveField(
            model_name='famestformdata',
            name='init_appl_pages_drawings',
        ),
        migrations.AddField(
            model_name='famestformdata',
            name='init_appl_details',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE,
                                       to='application.appldetails'),
            preserve_default=False,
        ),
    ]
