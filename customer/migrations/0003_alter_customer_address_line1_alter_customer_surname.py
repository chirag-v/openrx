# customer/migrations/0003_alter_customer_address_line1_alter_customer_surname.py
# Generated by Django 5.0.7 on 2024-07-17 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0002_remove_customer_address_customer_address_line1_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='address_line1',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='customer',
            name='surname',
            field=models.CharField(max_length=100),
        ),
    ]
