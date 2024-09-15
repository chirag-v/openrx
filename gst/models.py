# gst/models.py
from django.db import models

class GSTRate(models.Model):
    percentage = models.FloatField(unique=True)
    description = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.percentage}% - {self.description}"

class GST(models.Model):
    rate = models.ForeignKey(GSTRate, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.rate)

class StateCode(models.Model):
    code = models.CharField(max_length=2, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.code} - {self.name}"