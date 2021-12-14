from django.db import migrations, models


def set_defaults(apps, schema_editor):
    FeeCategory = apps.get_model("estimation", "feecategory")
    x = FeeCategory.objects.create(name='')
    x.save()


def reverse_func(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ('estimation', '0032_feecategory'),
    ]

    operations = [
        migrations.RunPython(set_defaults, reverse_func),

    ]
