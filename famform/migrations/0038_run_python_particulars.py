from django.db import migrations, models

from characteristics.models import DocFormat


def set_defaults(apps, schema_editor):
    ApplOptions = apps.get_model("famform", "ApplOptions")
    # df = DocFormat.objects.get(id=1)
    # print('df', df)
    for x in ApplOptions.objects.all().iterator():
        ApplOptionsParticulars = apps.get_model("famform", "ApplOptionsParticulars")
        applOptionsParticulars = ApplOptionsParticulars.objects.create(
            request_examination_early_bool=False,
            doc_format_id=1,
        )
        # x.appl
        x.save()


def reverse_func(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ('famform', '0037_auto_20211130_2240'),
    ]

    operations = [
        migrations.RunPython(set_defaults, reverse_func),
        # migrations.AlterField(
        #     model_name='famestformdata',
        #     name='init_appl_details',
        #     field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='application.appldetails'),
        # ),
    ]
