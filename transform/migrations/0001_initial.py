# Generated by Django 3.2.9 on 2021-12-15 21:09

from django.db import migrations, models
import django.db.models.deletion
import relativedeltafield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('characteristics', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DefaultCountryOANum',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('oa_total', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='OATransform',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_diff', relativedeltafield.fields.RelativeDeltaField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TransComplexTime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='USOATransform',
            fields=[
                ('oatransform_ptr',
                 models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True,
                                      primary_key=True, serialize=False, to='transform.oatransform')),
                ('final_oa_bool', models.BooleanField(default=False)),
            ],
            bases=('transform.oatransform',),
        ),
        migrations.CreateModel(
            name='RequestExaminationTransform',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_diff', relativedeltafield.fields.RelativeDeltaField()),
                ('complex_time_conditions',
                 models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE,
                                   to='transform.transcomplextime')),
                ('country',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='characteristics.country')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PublicationTransform',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_diff', relativedeltafield.fields.RelativeDeltaField()),
                ('complex_time_conditions',
                 models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE,
                                   to='transform.transcomplextime')),
                ('country',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='characteristics.country')),
            ],
        ),
        migrations.AddField(
            model_name='oatransform',
            name='complex_time_conditions',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE,
                                    to='transform.transcomplextime'),
        ),
        migrations.AddField(
            model_name='oatransform',
            name='country',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='characteristics.country'),
        ),
        migrations.CreateModel(
            name='IssueTransform',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_diff', relativedeltafield.fields.RelativeDeltaField()),
                ('complex_time_conditions',
                 models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE,
                                   to='transform.transcomplextime')),
                ('country',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='characteristics.country')),
            ],
        ),
        migrations.CreateModel(
            name='DefaultRequestExaminationTransform',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_diff', relativedeltafield.fields.RelativeDeltaField()),
                ('appl_type',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='characteristics.appltype')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DefaultPublTransform',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_diff', relativedeltafield.fields.RelativeDeltaField()),
                ('appl_type',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='characteristics.appltype')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DefaultOATransform',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_diff', relativedeltafield.fields.RelativeDeltaField()),
                ('appl_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='characteristics.appltype')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DefaultIssueTransform',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_diff', relativedeltafield.fields.RelativeDeltaField()),
                ('appl_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='characteristics.appltype')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DefaultFilingTransform',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_diff', relativedeltafield.fields.RelativeDeltaField()),
                ('appl_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='characteristics.appltype')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DefaultAllowanceTransform',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_diff', relativedeltafield.fields.RelativeDeltaField()),
                ('appl_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='characteristics.appltype')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CustomFilingTransform',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_diff', relativedeltafield.fields.RelativeDeltaField()),
                ('appl_type',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='characteristics.appltype')),
                ('complex_time_conditions',
                 models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE,
                                   to='transform.transcomplextime')),
                ('country',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='characteristics.country')),
                ('prev_appl_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE,
                                                     related_name='prev_appl_type', to='characteristics.appltype')),
            ],
        ),
        migrations.CreateModel(
            name='CountryOANum',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('oa_total', models.IntegerField()),
                ('country',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='characteristics.country')),
            ],
        ),
        migrations.CreateModel(
            name='AllowanceTransform',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_diff', relativedeltafield.fields.RelativeDeltaField()),
                ('complex_time_conditions',
                 models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE,
                                   to='transform.transcomplextime')),
                ('country',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='characteristics.country')),
            ],
        ),
        migrations.AddConstraint(
            model_name='usoatransform',
            constraint=models.UniqueConstraint(fields=('final_oa_bool',), name='FinalOABoolUniqueConstraint'),
        ),
        migrations.AddConstraint(
            model_name='publicationtransform',
            constraint=models.UniqueConstraint(fields=('country',), name='PublicationCountryUniqueConstraint'),
        ),
        migrations.AddConstraint(
            model_name='issuetransform',
            constraint=models.UniqueConstraint(fields=('country',), name='IssueCountryUniqueConstraint'),
        ),
        migrations.AddConstraint(
            model_name='customfilingtransform',
            constraint=models.UniqueConstraint(fields=('appl_type', 'prev_appl_type', 'country'),
                                               name='applicationTypePrevApplTypeCountryUniqueConstraint'),
        ),
        migrations.AddConstraint(
            model_name='countryoanum',
            constraint=models.UniqueConstraint(fields=('country',), name='CountryOANumCountryUniqueConstraint'),
        ),
        migrations.AddConstraint(
            model_name='allowancetransform',
            constraint=models.UniqueConstraint(fields=('country',), name='AllowanceCountryUniqueConstraint'),
        ),
    ]
