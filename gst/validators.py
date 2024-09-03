# gst/validators.py

from django.core.validators import RegexValidator

gstin_validator = RegexValidator(
    r'^\d{2}[A-Za-z0-9]{11}Z[A-Za-z0-9]$',
    'GSTIN must be 15 characters long, start with 2 numbers, have Z as the 14th character, and contain only numbers and alphabets.'
)