from django.db import migrations, models

from characteristics.models import DocFormat


def set_defaults(apps, schema_editor):
    ApplOptions = apps.get_model("famform", "ApplOptions")
    for x in ApplOptions.objects.all().iterator():
        ApplOptionsParticulars = apps.get_model("famform", "ApplOptionsParticulars")
        applOptionsParticulars = ApplOptionsParticulars.objects.create(
            request_examination_early_bool=False,
            doc_format_id=1,
        )
        x.particulars = applOptionsParticulars
        x.save()


def reverse_func(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ('famform', '0039_apploptions_particulars'),
    ]

    operations = [
        migrations.RunPython(set_defaults, reverse_func),
    ]
