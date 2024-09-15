# gst/management/commands/populate_gst_rates.py
from django.core.management.base import BaseCommand
from gst.models import GSTRate

class Command(BaseCommand):
    help = 'Populate the GSTRate model with predefined GST rates'

    def handle(self, *args, **kwargs):
        gst_rates = [
            (0.0, '0%'),
            (5.0, '5%'),
            (12.0, '12%'),
            (18.0, '18%'),
            (28.0, '28%'),
        ]

        for percentage, description in gst_rates:
            GSTRate.objects.get_or_create(percentage=percentage, defaults={'description': description})

        self.stdout.write(self.style.SUCCESS('Successfully populated GST rates'))