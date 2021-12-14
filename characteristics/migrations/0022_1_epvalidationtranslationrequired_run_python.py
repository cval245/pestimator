from django.db import migrations, models


def set_defaults(apps, schema_editor):
    TranslationImplementedPseudoEnum = apps.get_model("characteristics", "translationimplementedpseudoenum")
    x = TranslationImplementedPseudoEnum.objects.create(name='')
    x.save()
    y = TranslationImplementedPseudoEnum.objects.create(name='')
    y.save()


def reverse_func(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ('characteristics', '0026_auto_20211204_0430'),
    ]

    operations = [
        migrations.RunPython(set_defaults, reverse_func),

    ]
