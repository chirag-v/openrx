# company/models.py
from django.core.validators import RegexValidator
from django.db import models
from django.core.exceptions import ValidationError
from supplier.models import Supplier

class Company(models.Model):
    name = models.CharField(max_length=255)
    suppliers = models.ManyToManyField(Supplier, related_name='companies', blank=True)
    medical_representative = models.OneToOneField('MedicalRepresentative', on_delete=models.CASCADE, related_name='company_med_rep', null=True, blank=True)

    def __str__(self):
        return self.name

class Division(models.Model):
    name = models.CharField(max_length=255)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='divisions')
    suppliers = models.ManyToManyField(Supplier, related_name='divisions', blank=True)
    medical_representative = models.OneToOneField('MedicalRepresentative', on_delete=models.CASCADE, related_name='division_med_rep', null=True, blank=True)

    class Meta:
        unique_together = ('company', 'name')

    def __str__(self):
        return f"({self.company.name}) - {self.name}"

    def delete(self, *args, **kwargs):
        if self.suppliers.exists() or self.medical_representative is not None:
            raise ValueError("Cannot delete division. It has suppliers or medical representative.")
        super(Division, self).delete(*args, **kwargs)

class MedicalRepresentative(models.Model):
    name = models.CharField(max_length=255)
    company = models.ForeignKey(Company, null=True, blank=True, on_delete=models.SET_NULL, related_name='medical_representatives')
    division = models.ForeignKey(Division, null=True, blank=True, on_delete=models.SET_NULL, related_name='medical_representatives')
    mobile_number = models.CharField(max_length=10, validators=[RegexValidator(r'^\d{10}$')])

    def clean(self):
        if not self.company and not self.division:
            raise ValidationError('A Medical Representative must belong to either a company or a division.')
        if self.company and self.division:
            raise ValidationError('A Medical Representative cannot belong to both a company and a division.')

    def __str__(self):
        return self.name