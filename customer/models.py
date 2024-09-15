# customer/models.py
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models
from gst.models import StateCode
from gst.validators import gstin_validator


class Customer(models.Model):
    TITLE_CHOICES = [
        ('Mr.', 'Mr.'),
        ('Mrs.', 'Mrs.'),
        ('Miss', 'Miss'),
        ('Master', 'Master'),
        ('Adv.', 'Advocate'),
        ('Dr.', 'Doctor'),
        ('M/s', 'Messrs'),
        ('Prof.', 'Professor'),
    ]
    title = models.CharField(max_length=10, choices=TITLE_CHOICES, null=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    surname = models.CharField(max_length=100, null=True, blank=True)
    firm_name = models.CharField(max_length=255, null=True, blank=True)
    address_line1 = models.CharField(max_length=255, default='Nagpur')
    address_line2 = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    landmark = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=35, null=True, blank=True)
    pincode = models.CharField(max_length=6, validators=[RegexValidator(r'^\d{1,6}$',
                                                                        'Only numeric characters are allowed.')],
                               null=True, blank=True)
    phone = models.CharField(max_length=20, validators=[RegexValidator(r'^\d{1,20}$',
                                                                       'Only numeric characters are allowed.')],
                             null=True, blank=True)
    mobile = models.CharField(max_length=10, validators=[RegexValidator(r'^\d{1,10}$',
                                                                        'Only numeric characters are allowed.')],
                        )
    TYPE_CHOICES = [
        ('b2b', 'B2B'),
        ('b2c', 'B2C'),
    ]
    type = models.CharField(max_length=3, choices=TYPE_CHOICES, default='b2c')
    CATEGORY_CHOICES = [
        ('wholesaler', 'Wholesaler'),
        ('retailer', 'Retailer'),
        ('superstockist', 'Superstockist'),
        ('bronze', 'Bronze'),
        ('silver', 'Silver'),
        ('gold', 'Gold'),
        ('platinum', 'Platinum'),
        ('not applicable', 'Not applicable'),
    ]
    category = models.CharField(max_length=15, choices=CATEGORY_CHOICES, default='not applicable')
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
    CURRENT_STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    current_status = models.CharField(max_length=8, choices=CURRENT_STATUS_CHOICES, default='active')

    # Add the __str__ method here to ensure it always returns a valid string
    def __str__(self):
        if self.name:
            return f"{self.title or ''} {self.name} {self.surname or ''}".strip()
        elif self.firm_name:
            return self.firm_name
        else:
            return 'Unknown Customer'


    @property
    def required_fields(self):
        if self.type == 'b2b':
            return {'firm_name': self.firm_name}
        elif self.type == 'b2c':
            return {'name': self.name, 'surname': self.surname}

    @property
    def category_options(self):
        if self.type == 'b2b':
            return ['wholesaler', 'retailer', 'superstockist', 'not applicable']
        elif self.type == 'b2c':
            return ['bronze', 'silver', 'gold', 'not applicable']
        else:
            return []

    @property
    def discount(self):
        if self.type == 'b2c':
            category_discounts = {
                'bronze': 4,
                'silver': 5,
                'gold': 10,
            }
            return category_discounts.get(self.category, 0)
        return 0


    def clean(self):
        super().clean()  # Call the base class clean method first
        type = self.type
        gst_registration = self.gst_registration
        gstin = self.gstin

        # Skip GSTIN validation for B2C customers and B2B customers who are Unregistered Dealers
        if not (type == 'b2c' or (type == 'b2b' and gst_registration == 'URD')) and not gstin:
            # For B2B customers with GST registration other than URD, GSTIN is required
            raise ValidationError({'gstin': 'GSTIN is required for registered and composition B2B customers.'})

        # Validate GSTIN format if provided
        if gstin:
            try:
                gstin_validator(gstin)
            except ValidationError as e:
                raise ValidationError({'gstin': e.message})



def save(self, *args, **kwargs):
    if self.gstin:
        self.state_code = self.gstin[:2]
        self.pan = self.gstin[2:12]
        state = StateCode.objects.filter(code=self.state_code).first()
        self.state = state.name if state else ''

    super(Customer, self).save(*args, **kwargs)


    @staticmethod
    def some_other_static_method(code):
        state = StateCode.objects.filter(code=code).first()
        return state.name if state else ''


    class Meta:
        verbose_name = "Customer"
        verbose_name_plural = "Customers"