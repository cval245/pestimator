# Generated by Django 3.2.3 on 2021-11-23 20:13

from django.db import migrations, models
import django.db.models.deletion
import relativedeltafield.fields


class Migration(migrations.Migration):
    dependencies = [
        ('famform', '0029_alter_famestformdata_init_appl_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='RequestExaminationOptions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_diff', relativedeltafield.fields.RelativeDeltaField()),
                ('appl', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='famform.apploptions')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
