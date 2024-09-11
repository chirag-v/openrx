# purchase/forms.py
from django import forms
from .models import Purchase, PurchaseItem
from supplier.models import Supplier


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
        purchase_type = cleaned_data.get('purchase_type')
        invoice_number = cleaned_data.get('invoice_number')
        invoice_date = cleaned_data.get('invoice_date')
        invoice_discount = cleaned_data.get('invoice_discount')
        if not supplier_name:
            raise forms.ValidationError('Supplier name is required')
        if not purchase_type:
            raise forms.ValidationError('Purchase type is required')
        if not invoice_number:
            raise forms.ValidationError('Invoice number is required')
        if not invoice_date:
            raise forms.ValidationError('Invoice date is required')
        return cleaned_data


class PurchaseItemForm(forms.ModelForm):
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
            'expiry_date': forms.DateInput(attrs={'type': 'date', 'id': 'expiry_date'}),
            'purchase_rate': forms.NumberInput(attrs={'class': 'form-control', 'id': 'purchase_rate'}),
            'item_discount_percentage': forms.NumberInput(attrs={'class': 'form-control', 'id': 'item_discount_percentage'}),
            'item_discount_amount': forms.NumberInput(attrs={'class': 'form-control', 'id': 'item_discount_amount'}),
        }