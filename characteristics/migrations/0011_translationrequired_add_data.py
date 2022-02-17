from datetime import date

from django.db import migrations


def forwards_func(apps, schema_editor):
    # We get the model from the versioned app registry;
    # if we directly import it, it'll be the wrong version
    TranslationRequiredOptions = apps.get_model("characteristics", "TranslationRequiredOptions")
    TranslationRequiredOptions.objects.create(name='full translation required')


def reverse_func(apps, schema_editor):
    # forwards_func() creates two Country instances,
    # so reverse_func() should delete them.
    # Country = apps.get_model("myapp", "Country")
    # db_alias = schema_editor.connection.alias
    # Country.objects.using(db_alias).filter(name="USA", code="us").delete()
    # Country.objects.using(db_alias).filter(name="France", code="fr").delete()
    pass


class Migration(migrations.Migration):
    dependencies = [
        ('characteristics', '0010_translationrequiredoptions_and_more'),
    ]
    operations = [
        migrations.RunPython(forwards_func, reverse_func),
    ]
