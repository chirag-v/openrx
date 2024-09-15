from datetime import datetime, timedelta
from django import forms
from django.core.exceptions import ValidationError
from .models import Purchase, PurchaseItem

class MMYYDateField(forms.DateField):
    def to_python(self, value):
        if not value:
            return None
        try:
            date = datetime.strptime(value, '%m/%y')
            next_month = date.replace(day=28) + timedelta(days=4)
            last_day_of_month = next_month - timedelta(days=next_month.day)
            return last_day_of_month.date()
        except ValueError:
            raise forms.ValidationError('Enter a valid date in mm/yy format.')

    def prepare_value(self, value):
        if isinstance(value, datetime):
            return value.strftime('%m/%y')
        return value

class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ['supplier_name', 'purchase_type', 'invoice_number', 'invoice_date', 'invoice_discount']
        widgets = {
            'supplier_name': forms.Select(attrs={'class': 'form-control', 'id': 'supplier-select'}),
            'purchase_type': forms.Select(attrs={'class': 'form-control'}),
            'invoice_date': forms.DateInput(attrs={'type': 'date'}),
            'invoice_number': forms.TextInput(attrs={'class': 'form-control'}),
            'invoice_discount': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        supplier_name = cleaned_data.get('supplier_name')
        invoice_number = cleaned_data.get('invoice_number')
        invoice_date = cleaned_data.get('invoice_date')
        financial_year_start = invoice_date.replace(month=4, day=1)
        financial_year_end = invoice_date.replace(year=invoice_date.year + 1, month=3, day=31)

        if not supplier_name:
            raise forms.ValidationError('Supplier name is required')
        if not cleaned_data.get('purchase_type'):
            raise forms.ValidationError('Purchase type is required')
        if not invoice_number:
            raise forms.ValidationError('Invoice number is required')
        if not invoice_date:
            raise forms.ValidationError('Invoice date is required')

        existing_purchases = Purchase.objects.filter(
            supplier_name=supplier_name,
            invoice_number=invoice_number,
            invoice_date__range=(financial_year_start, financial_year_end)
        ).exclude(pk=self.instance.pk)

        if existing_purchases.exists():
            raise ValidationError('Invoice number must be unique for the given supplier in the financial year.')

        return cleaned_data

class PurchaseItemForm(forms.ModelForm):
    expiry_date = MMYYDateField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'mm/yy'}))

    class Meta:
        model = PurchaseItem
        fields = ['item', 'mrp', 'quantity', 'free', 'batch_number', 'expiry_date', 'purchase_rate',
                  'item_discount_percentage', 'item_discount_amount']
        widgets = {
            'item': forms.Select(attrs={'class': 'form-control', 'id': 'item-select'}),
            'mrp': forms.NumberInput(attrs={'class': 'form-control', 'id': 'mrp'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'id': 'quantity'}),
            'free': forms.NumberInput(attrs={'class': 'form-control', 'id': 'free'}),
            'batch_number': forms.TextInput(attrs={'class': 'form-control', 'id': 'batch_number'}),
            'purchase_rate': forms.NumberInput(attrs={'class': 'form-control', 'id': 'purchase_rate'}),
            'item_discount_percentage': forms.NumberInput(attrs={'class': 'form-control', 'id': 'item_discount_percentage'}),
            'item_discount_amount': forms.NumberInput(attrs={'class': 'form-control', 'id': 'item_discount_amount'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        required_fields = ['item', 'mrp', 'quantity', 'batch_number', 'expiry_date', 'purchase_rate']
        for field in required_fields:
            if not cleaned_data.get(field):
                raise forms.ValidationError(f'{field.replace("_", " ").capitalize()} is required')
        return cleaned_data