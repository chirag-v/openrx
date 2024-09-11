# supplier/models.py
from django.core.validators import RegexValidator
from django.db import models

import gst
from gst.utils import get_state_name_by_code


class Supplier(models.Model):
    name = models.CharField(max_length=255)
    address_line1 = models.CharField(max_length=255, blank=True, null=True)
    address_line2 = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    landmark = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=35, null=True, blank=True)
    pincode = models.CharField(max_length=6, null=True, blank=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=20, validators=[RegexValidator(r'^\d{1,20}$',
                                                                       'Only numeric characters are allowed.')],
                             null=True, blank=True)
    phone2 = models.CharField(max_length=20, validators=[RegexValidator(r'^\d{1,20}$',
                                                                        'Only numeric characters are allowed.')],
                              null=True, blank=True)
    phone3 = models.CharField(max_length=20, validators=[RegexValidator(r'^\d{1,20}$',
                                                                        'Only numeric characters are allowed.')],
                              null=True, blank=True)
    mobile = models.CharField(max_length=10, validators=[RegexValidator(r'^\d{1,10}$',
                                                                        'Only numeric characters are allowed.')], blank=True, null=True)
    owner_name = models.CharField(max_length=100, null=True, blank=True)
    owner_mobile = models.CharField(max_length=10, validators=[RegexValidator(r'^\d{1,10}$',
                                                                                'Only numeric characters are allowed.')], blank=True, null=True)
    manager_name = models.CharField(max_length=100, null=True, blank=True)
    manager_mobile = models.CharField(max_length=10, validators=[RegexValidator(r'^\d{1,10}$',
                                                                                    'Only numeric characters are allowed.')], blank=True, null=True)

    GST_REGISTRATION_CHOICES = [
        ('registered', 'Registered'),
        ('composition', 'Composition'),
        ('URD', 'Unregistered Dealer'),
    ]
    gst_registration = models.CharField(max_length=11, choices=GST_REGISTRATION_CHOICES, null=True, blank=True)
    gstin = models.CharField(max_length=15, validators=[RegexValidator(
        r'^\d{2}[A-Za-z0-9]{11}Z[A-Za-z0-9]$',
        'GSTIN must be 15 characters long, start with 2 numbers, have Z as the 14th character, and contain only '
        'numbers and alphabets.'
    )], null=True, blank=True)
    state_code = models.CharField(max_length=2, null=True, blank=True)
    state = models.CharField(max_length=50, null=True, blank=True)
    pan = models.CharField(max_length=10, null=True, blank=True)
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]
    drug_license1 = models.CharField(max_length=50, null=True, blank=True)
    drug_license1_validity = models.DateField(null=True, blank=True)
    drug_license2 = models.CharField(max_length=50, null=True, blank=True)
    drug_license2_validity = models.DateField(null=True, blank=True)
    food_registration = models.CharField(max_length=50, null=True, blank=True)
    food_registration_validity = models.DateField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default='active')

    def clean(self):
        super().clean()  # Call the base class clean method first
        if self.gstin:
            self.state_code = self.gstin[:2]
            self.pan = self.gstin[2:12]
            self.state = gst.utils.get_state_name_by_code(self.state_code)

    def save(self, *args, **kwargs):
        if self.gstin:
            self.state_code = self.gstin[:2]
            self.pan = self.gstin[2:12]
            self.state = gst.utils.get_state_name_by_code(self.state_code)
        super(Supplier, self).save(*args, **kwargs)

    @staticmethod
    def some_other_static_method(code):
        state_name = get_state_name_by_code(code)
        return state_name

    def __str__(self):
        return self.name
