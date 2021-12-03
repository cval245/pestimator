# Generated by Django 3.2.3 on 2021-11-29 17:39

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('characteristics', '0015_auto_20211128_1842'),
    ]

    operations = [
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('words_per_page', models.IntegerField()),
            ],
        ),
        migrations.RemoveField(
            model_name='languages',
            name='country',
        ),
    ]
