from django.db import migrations, models


def set_defaults(apps, schema_editor):
    FamEstFormData = apps.get_model("famform", "FamEstFormData")
    for x in FamEstFormData.objects.all().iterator():
        CustomApplOptions = apps.get_model("famform", "CustomApplOptions")
        # ApplDetails.objects.all()
        customApplOptions = CustomApplOptions.objects.create(
            request_examination_early_bool=False
        )

        # applDetails.save()
        x.init_appl_options = customApplOptions
        x.save()


def reverse_func(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ('famform', '0027_auto_20211122_2038'),
    ]

    operations = [
        migrations.RunPython(set_defaults, reverse_func),
        # migrations.AlterField(
        #     model_name='famestformdata',
        #     name='init_appl_details',
        #     field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='application.appldetails'),
        # ),
    ]
