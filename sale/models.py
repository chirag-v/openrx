# sale/models.py
from django.db import models
from decimal import Decimal
from customer.models import Customer
from gst.models import GST
from django.utils.translation import gettext_lazy as _


class Sale(models.Model):
    class PaymentMethod(models.TextChoices):
        CASH = 'cash', _('Cash')
        CARD = 'card', _('Card')
        ONLINE = 'online', _('Online')

    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    sale_date = models.DateTimeField(null=True, blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    bill_discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0.00'))
    line_discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0.00'))
    net_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    payment_method = models.CharField(max_length=10, choices=PaymentMethod.choices)
    payment_status = models.BooleanField(default=False)
    invoice_number = models.CharField(max_length=50, unique=True, blank=True, null=True)
    gst = models.ForeignKey(GST, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        # Automatically calculate total_amount and net_amount before saving
        self.calculate_total_amount()
        self.calculate_net_amount()
        super(Sale, self).save(*args, **kwargs)
        if not self.invoice_number:
            self.invoice_number = f"INV{self.id:06d}"
            super(Sale, self).save(update_fields=['invoice_number'])

    def calculate_total_amount(self):
        """Calculate the total amount of the sale from its items."""
        total = sum(item.amount for item in self.saleitem_set.all())
        self.total_amount = total

    def calculate_net_amount(self):
        """Calculate the net amount by applying percentage discounts."""
        # Apply line discount to total amount
        line_discount_amount = (self.total_amount * self.line_discount_percentage) / 100
        discounted_total = self.total_amount - line_discount_amount

        # Apply bill discount to the discounted total
        bill_discount_amount = (discounted_total * self.bill_discount_percentage) / 100
        self.net_amount = discounted_total - bill_discount_amount

    def __str__(self):
        customer_name = self.customer.name if self.customer and self.customer.name else 'Walk-in Customer'
        return f"Sale {self.invoice_number or 'No Invoice'} - {customer_name}"


class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    item = models.ForeignKey('item.Item', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0.00'))
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))

    def save(self, *args, **kwargs):
        # Calculate the discount and final amount for this line item
        if self.discount_percentage and not self.discount_amount:
            self.discount_amount = (self.selling_price * self.quantity) * (self.discount_percentage / 100)
        elif self.discount_amount and not self.discount_percentage:
            self.discount_percentage = (self.discount_amount / (self.selling_price * self.quantity)) * 100

        total_price = self.selling_price * self.quantity
        discounted_price = total_price - self.discount_amount
        gst_amount = discounted_price * (Decimal(self.item.gst.percentage) / Decimal(100))
        self.amount = discounted_price + gst_amount

        super().save(*args, **kwargs)

    def __str__(self):
        item_name = self.item.name if self.item and self.item.name else 'Unknown Item'
        sale_invoice = self.sale.invoice_number if self.sale and self.sale.invoice_number else 'No Sale'
        return f"{item_name} in Sale {sale_invoice}"
