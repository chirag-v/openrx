# item/forms.py
from django import forms
from django.core.validators import RegexValidator

from gst.models import GST
from .models import Item
from company.models import Company, Division


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'item_type', 'sku', 'image', 'sold_loose', 'sold_online', 'mrp', 'purchase_price',
                  'selling_price', 'landing_cost', 'use', 'weight', 'company', 'division', 'dosage_form', 'packing',
                  'strength', 'batch_number', 'expiry_date', 'prescription_required', 'gst', 'hsn']
        widgets = {
            'item_type': forms.RadioSelect(attrs={'class': 'type-radio'}, choices=Item.ITEM_TYPE_CHOICES),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'sku': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'mrp': forms.NumberInput(attrs={'class': 'form-control'}),
            'purchase_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'selling_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'landing_cost': forms.NumberInput(attrs={'class': 'form-control'}),
            'use': forms.TextInput(attrs={'class': 'form-control'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control'}),
            'sold_loose': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'sold_online': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'dosage_form': forms.TextInput(attrs={'class': 'form-control'}),
            'packing': forms.TextInput(attrs={'class': 'form-control'}),
            'strength': forms.TextInput(attrs={'class': 'form-control'}),
            'batch_number': forms.TextInput(attrs={'class': 'form-control'}),
            'expiry_date': forms.DateInput(attrs={'class': 'form-control'}),
            'prescription_required': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'gst': forms.Select(attrs={'class': 'form-control'}, choices=[(gst.id, f"{gst.percentage}%") for gst
                                                                          in GST.objects.all()]),
            'company': forms.Select(attrs={'class': 'form-control', 'data-url': '/company/get-divisions/'}),
            'division': forms.Select(attrs={'class': 'form-control'}),
            'hsn': forms.TextInput(attrs={'class': 'form-control'}),
        }


        labels = {
            'name': 'Item Name',
            'item_type': 'Item Type',
            'sku': 'SKU',
            'image': 'Image',
            'mrp': 'MRP',
            'purchase_price': 'Purchase Price',
            'selling_price': 'Selling Price',
            'landing_cost': 'Landing Cost',
            'use': 'Use',
            'weight': 'Weight',
            'sold_loose': 'Sold Loose',
            'sold_online': 'Sold Online',
            'dosage_form': 'Dosage Form',
            'packing': 'Packing',
            'strength': 'Strength',
            'batch_number': 'Batch Number',
            'expiry_date': 'Expiry Date',
            'prescription_required': 'Prescription Required',
            'gst': 'GST',
            'company': 'Company',
            'division': 'Division',
            'hsn': 'HSN',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            default_gst = GST.objects.get(percentage=12.0)
            self.fields['gst'].initial = default_gst.id
        except GST.DoesNotExist:
            pass
