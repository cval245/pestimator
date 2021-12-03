from django.db import migrations, models


def set_defaults(apps, schema_editor):
    FamEstFormData = apps.get_model("famform", "FamEstFormData")
    for x in FamEstFormData.objects.all().iterator():
        PCTMethodCustomization = apps.get_model("famform", "PCTMethodCustomization")
        EPMethodCustomization = apps.get_model("famform", "EPMethodCustomization")
        if x.pct_method_customization is None:
            x.pct_method_customization = PCTMethodCustomization.objects.create(
                custom_appl_details=None,
                custom_appl_options=None,
            )

        if x.ep_method_customization is None:
            x.ep_method_customization = EPMethodCustomization.objects.create(
                custom_appl_details=None,
                custom_appl_options=None, )
        x.save()


def reverse_func(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ('famform', '0041_alter_apploptions_particulars'),
    ]

    operations = [
        migrations.RunPython(set_defaults, reverse_func),
    ]
