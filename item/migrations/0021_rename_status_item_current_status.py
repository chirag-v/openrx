# Generated by Django 5.1.1 on 2024-09-15 12:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0020_item_hsn'),
    ]

    operations = [
        migrations.RenameField(
            model_name='item',
            old_name='status',
            new_name='current_status',
        ),
    ]
