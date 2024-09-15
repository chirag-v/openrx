# item/models.py
from django.core.validators import RegexValidator
from django.db import models
from company.models import Company, Division
from gst.models import GST

class Item(models.Model):
    ITEM_TYPE_CHOICES = [
        ('medicine', 'Medicine'),
        ('nonmedicalitem', 'Non-Medical Item')
    ]

    name = models.CharField(max_length=255)
    item_type = models.CharField(max_length=50, choices=ITEM_TYPE_CHOICES, default='medicine')
    sku_validator = RegexValidator(r'^\d{0,10}$', 'SKU must be between 0 to 10 digits')
    sku = models.CharField(max_length=10, unique=True, validators=[sku_validator])
    image = models.ImageField(upload_to='item_images/', null=True, blank=True)
    sold_loose = models.BooleanField(default=False)
    sold_online = models.BooleanField(default=False)
    mrp = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    landing_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    use = models.CharField(max_length=255, null=True, blank=True)
    weight = models.DecimalField(max_digits=10, decimal_places=2)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    division = models.ForeignKey(Division, on_delete=models.CASCADE, null=True, blank=True)
    current_status = models.CharField(max_length=1, choices=[('A', 'Active'), ('D', 'Discontinued'), ('B', "Banned")], default='A')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    gst = models.ForeignKey(GST, on_delete=models.CASCADE)
    hsn = models.CharField(max_length=8,
                           validators=[RegexValidator(r'^\d{2,8}$', 'HSN must be 2 to 8 digits')],
                           null=True, blank=True)

    # Medicine specific fields (hide via javascript in frontend when item_type is nonmedicalitem)
    dosage_form = models.CharField(max_length=100, null=True, blank=True)
    packing = models.CharField(max_length=100, null=True, blank=True)
    strength = models.CharField(max_length=100, null=True, blank=True)
    batch_number = models.CharField(max_length=100, null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    prescription_required = models.BooleanField(default=True, null=True, blank=True)


    def __str__(self):
        return self.name