# gst/migrations/0006_delete_hsn.py
# Generated by Django 5.0.7 on 2024-07-31 22:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gst', '0005_alter_hsn_hsn_code'),
        ('item', '0019_remove_item_hsn'),
    ]

    operations = [
        migrations.DeleteModel(
            name='HSN',
        ),
    ]
