# Generated by Django 3.2.3 on 2021-11-28 18:42

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('estimation', '0031_lineestimationtemplateconditions_doc_format'),
    ]

    operations = [
        migrations.CreateModel(
            name='FeeCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
    ]
