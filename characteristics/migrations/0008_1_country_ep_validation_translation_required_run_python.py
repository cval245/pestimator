from django.db import migrations, models


def set_defaults(apps, schema_editor):
    EPValidationTranslationRequired = apps.get_model("characteristics", "epvalidationtranslationrequired")
    x = EPValidationTranslationRequired.objects.create(name='')
    x.save()


def reverse_func(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ('characteristics', '0007_auto_20211022_2031'),
    ]

    operations = [
        migrations.RunPython(set_defaults, reverse_func),

    ]
