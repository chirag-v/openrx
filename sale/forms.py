# sales/forms.py
from django import forms
from .models import Sale, SaleItem


class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['customer', 'payment_method', 'payment_status', 'bill_discount_percentage', 'line_discount_percentage', 'sale_date']
        widgets = {
            'customer': forms.Select(attrs={'class': 'form-control', 'id': 'customer-select'}),
            'payment_method': forms.Select(attrs={'class': 'form-control'}),
            'bill_discount_percentage': forms.NumberInput(attrs={'class': 'form-control'}),
            'line_discount_percentage': forms.NumberInput(attrs={'class': 'form-control'}),
            'sale_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        customer = cleaned_data.get('customer')
        payment_method = cleaned_data.get('payment_method')
        discount_amount = cleaned_data.get('discount_amount')

        if not customer:
            raise forms.ValidationError('Customer is required')
        if not payment_method:
            raise forms.ValidationError('Payment method is required')
        return cleaned_data

class SaleItemForm(forms.ModelForm):
    class Meta:
        model = SaleItem
        fields = ['item', 'quantity', 'selling_price', 'discount_percentage', 'discount_amount']
        widgets = {
            'item': forms.Select(attrs={'class': 'form-control', 'id': 'item-select'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'id': 'quantity'}),
            'selling_price': forms.NumberInput(attrs={'class': 'form-control', 'id': 'selling_price'}),
            'discount_percentage': forms.NumberInput(attrs={'class': 'form-control', 'id': 'discount_percentage'}),
            'discount_amount': forms.NumberInput(attrs={'class': 'form-control', 'id': 'discount_amount'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        item = cleaned_data.get('item')
        quantity = cleaned_data.get('quantity')
        selling_price = cleaned_data.get('selling_price')

        if not item:
            raise forms.ValidationError('Item is required')
        if not quantity or quantity <= 0:
            raise forms.ValidationError('Quantity must be greater than zero')
        if not selling_price or selling_price <= 0:
            raise forms.ValidationError('Selling price must be greater than zero')
        return cleaned_data
