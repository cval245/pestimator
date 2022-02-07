from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('characteristics', '0006_detailedfeecategory_country'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='detailedfeecategory',
            constraint=models.UniqueConstraint(
                fields=['name', 'country'],
                name='UniqueNameCountryConstraint',
            )
        )
    ]
