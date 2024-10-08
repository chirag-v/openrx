# Generated by Django 5.1.1 on 2024-09-13 22:45

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0006_alter_medicalrepresentative_mobile_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='medicalrepresentative',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='medical_representatives', to='company.company'),
        ),
        migrations.AddField(
            model_name='medicalrepresentative',
            name='division',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='medical_representatives', to='company.division'),
        ),
        migrations.AlterField(
            model_name='company',
            name='medical_representative',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='company_med_rep', to='company.medicalrepresentative'),
        ),
        migrations.AlterField(
            model_name='company',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='division',
            name='medical_representative',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='division_med_rep', to='company.medicalrepresentative'),
        ),
        migrations.AlterField(
            model_name='medicalrepresentative',
            name='mobile_number',
            field=models.CharField(max_length=10, validators=[django.core.validators.RegexValidator('^\\d{10}$')]),
        ),
    ]
