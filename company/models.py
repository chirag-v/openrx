# In company/models.py
from django.core.validators import RegexValidator
from django.db import models
from supplier.models import Supplier


class MedicalRepresentative(models.Model):
    name = models.CharField(max_length=255)
    mobile_number = models.CharField(max_length=10, validators=[RegexValidator(r'^\d{1,10}$',
                                                                        'Only numeric characters are allowed.')],
                                     )

    def __str__(self):
        return self.name


class Company(models.Model):
    name = models.CharField(max_length=255, unique=True)
    suppliers = models.ManyToManyField(Supplier, related_name='companies', blank=True)
    medical_representative = models.OneToOneField(MedicalRepresentative, null=True, blank=True,
                                                   on_delete=models.CASCADE, related_name='company')

    # Other fields as necessary

    def __str__(self):
        return self.name


class Division(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='divisions')
    name = models.CharField(max_length=255)
    suppliers = models.ManyToManyField(Supplier, related_name='divisions', blank=True)
    medical_representative = models.OneToOneField(MedicalRepresentative, on_delete=models.CASCADE,
                                                  related_name='division', null=True, blank=True)

    class Meta:
        unique_together = ('company', 'name')


    def __str__(self):
        return f"({self.company.name}) - {self.name}"

    def delete(self, *args, **kwargs):
        if self.suppliers.exists() or self.medical_representative is not None:
            raise ValueError("Cannot delete division. It has suppliers or medical representative.")
        super(Division,self).delete(*args, **kwargs)

