from django import forms
from .models import Purchase, PurchaseItem


class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ['supplier_name', 'purchase_type', 'invoice_number', 'invoice_date', 'invoice_discount']
        widgets = {
            'supplier_name': forms.Select(attrs={'class': 'form-control', 'id': 'supplier-select'}),
            'purchase_type': forms.Select(attrs={'class': 'form-control'}),
            'invoice_date': forms.DateInput(attrs={'type': 'date'}),
            'invoice_number': forms.TextInput(attrs={'class': 'form-control'}),
            'invoice_discount': forms.NumberInput(attrs={'class': 'form-control'})

        }


class PurchaseItemForm(forms.ModelForm):
    class Meta:
        model = PurchaseItem
        fields = ['item', 'mrp', 'quantity', 'free', 'batch_number', 'expiry_date', 'purchase_rate',
                  'item_discount_percentage', 'item_discount_amount']