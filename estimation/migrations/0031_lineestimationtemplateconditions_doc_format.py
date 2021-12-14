# Generated by Django 3.2.3 on 2021-11-24 15:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('characteristics', '0011_1_docformat_run_python'),
        ('estimation', '0030_requestexamest'),
    ]

    operations = [
        migrations.AddField(
            model_name='lineestimationtemplateconditions',
            name='doc_format',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE,
                                    to='characteristics.docformat'),
        ),
    ]
