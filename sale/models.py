from django.db import models
from django.core.validators import RegexValidator
from decimal import Decimal
from customer.models import Customer
from item.models import Item
from django.utils.translation import gettext_lazy as _


class Sale(models.Model):
    class PaymentMethod(models.TextChoices):
        CASH = 'cash', _('Cash')
        CARD = 'card', _('Card')
        ONLINE = 'online', _('Online')

    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    sale_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    net_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    payment_method = models.CharField(max_length=10, choices=PaymentMethod.choices)
    payment_status = models.BooleanField(default=False)
    invoice_number = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"Sale {self.invoice_number} - {self.customer.name if self.customer else 'Walk-in Customer'}"


class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0.00'))
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))

    def save(self, *args, **kwargs):
        if self.discount_percentage and not self.discount_amount:
            self.discount_amount = (self.selling_price * self.quantity) * (self.discount_percentage / 100)
        elif self.discount_amount and not self.discount_percentage:
            self.discount_percentage = (self.discount_amount / (self.selling_price * self.quantity)) * 100

        total_price = (self.selling_price * self.quantity)
        discounted_price = total_price - self.discount_amount
        gst_amount = discounted_price * (Decimal(self.item.gst.percentage) / Decimal(100))
        self.amount = discounted_price + gst_amount

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.item.name} in Sale {self.sale.invoice_number}"
