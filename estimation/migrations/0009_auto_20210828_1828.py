# Generated by Django 3.2.3 on 2021-08-28 18:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('estimation', '0008_lineestimationtemplateconditions_condition_annual_prosecution_fee'),
    ]

    operations = [
        migrations.CreateModel(
            name='ComplexTimeConditions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='lineestimationtemplateconditions',
            name='condition_time_complex',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE,
                                    to='estimation.complextimeconditions'),
        ),
    ]