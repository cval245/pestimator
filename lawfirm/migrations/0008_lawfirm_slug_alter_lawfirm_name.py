# Generated by Django 4.0.2 on 2022-03-17 07:01

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('lawfirm', '0007_lawfirm_lawfirmnameuniqueconstraint'),
    ]

    operations = [
        migrations.AddField(
            model_name='lawfirm',
            name='slug',
            field=models.SlugField(default=1, max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='lawfirm',
            name='name',
            field=models.CharField(max_length=255),
        ),
    ]
