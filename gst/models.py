# gst/models.py
from django.db import models

class GST(models.Model):
    GST_RATES = [
        (0.0, '0%'),
        (5.0, '5%'),
        (12.0, '12%'),
        (18.0, '18%'),
        (28.0, '28%'),
    ]

    percentage = models.FloatField(choices=GST_RATES, unique=True)

    def __str__(self):
        return f"{self.percentage}%"


class StateCode(models.Model):
    code = models.CharField(max_length=2, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.code} - {self.name}"
