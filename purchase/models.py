from django.db import models
from django.core.validators import MinValueValidator
from item.models import Item
from supplier.models import Supplier

class Purchase(models.Model):
    PURCHASE_TYPE_CHOICES = [
        ('cash', 'Cash'),
        ('credit', 'Credit')
    ]
    supplier_name = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    purchase_type = models.CharField(max_length=6, choices=PURCHASE_TYPE_CHOICES)
    invoice_number = models.CharField(max_length=50, unique=True)
    invoice_date = models.DateField()
    grn_date = models.DateField(auto_now_add=True)
    gross_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    invoice_discount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    net_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def calculate_gross_amount(self):
        self.gross_amount = sum(item.amount for item in self.purchaseitem_set.all())
        self.save()

    def calculate_net_amount(self):
        self.net_amount = self.gross_amount - self.invoice_discount
        self.save()

    def __str__(self):
        return f"Purchase {self.invoice_number} from {self.supplier_name}"


class PurchaseItem(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    mrp = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    free = models.PositiveIntegerField(default=0)
    batch_number = models.CharField(max_length=100)
    expiry_date = models.DateField()
    purchase_rate = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    item_discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    item_discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def calculate_amount(self):
        discount_from_percentage = (self.purchase_rate * self.quantity) * (self.item_discount_percentage / 100)
        total_discount = discount_from_percentage + self.item_discount_amount
        discounted_amount = (self.purchase_rate * self.quantity) - total_discount
        gst_amount = discounted_amount * (self.item.gst.percentage / 100)
        self.amount = discounted_amount + gst_amount
        self.save()

    def __str__(self):
        return f"{self.item.name} in Purchase {self.purchase.invoice_number}"