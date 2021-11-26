from django.db import migrations, models


def set_defaults(apps, schema_editor):
    ApplOptions = apps.get_model("famform", "apploptions")
    for x in ApplOptions.objects.all().iterator():
        CustomApplOptions = apps.get_model("famform", "CustomApplOptions")
        customApplOptions = CustomApplOptions.objects.create(
            request_examination_early_bool=False,
            doc_format_id=1
        )

        # applDetails.save()
        x.custom_appl_options = customApplOptions
        x.save()


def reverse_func(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ('famform', '0032_auto_20211124_1509'),
    ]

    operations = [
        migrations.RunPython(set_defaults, reverse_func),
        # migrations.AlterField(
        #     model_name='famestformdata',
        #     name='init_appl_details',
        #     field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='application.appldetails'),
        # ),
    ]
