from django.db import migrations, models


def set_defaults(apps, schema_editor):
    DocFormat = apps.get_model("characteristics", "docformat")
    x = DocFormat.objects.create(name='')
    x.save()


def reverse_func(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ('characteristics', '0011_docformat'),
    ]

    operations = [
        migrations.RunPython(set_defaults, reverse_func),

    ]
