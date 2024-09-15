from django.core.exceptions import ValidationError
from django.forms import ModelForm, RadioSelect, TextInput, FileInput, DateInput, CheckboxInput, Select, NumberInput

from company.models import Company, Division
from gst.models import GST
from item.models import Item


class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'item_type', 'sku', 'image', 'sold_loose', 'sold_online', 'mrp', 'purchase_price',
                  'selling_price', 'landing_cost', 'use', 'weight', 'company', 'division', 'dosage_form', 'packing',
                  'strength', 'batch_number', 'expiry_date', 'prescription_required', 'gst', 'hsn']
        widgets = {
            'item_type': RadioSelect(attrs={'class': 'type-radio'}, choices=Item.ITEM_TYPE_CHOICES),
            'name': TextInput(attrs={'class': 'form-control'}),
            'sku': TextInput(attrs={'class': 'form-control'}),
            'image': FileInput(attrs={'class': 'form-control'}),
            'mrp': NumberInput(attrs={'class': 'form-control'}),
            'purchase_price': NumberInput(attrs={'class': 'form-control'}),
            'selling_price': NumberInput(attrs={'class': 'form-control'}),
            'landing_cost': NumberInput(attrs={'class': 'form-control'}),
            'use': TextInput(attrs={'class': 'form-control'}),
            'weight': NumberInput(attrs={'class': 'form-control'}),
            'sold_loose': CheckboxInput(attrs={'class': 'form-check-input'}),
            'sold_online': CheckboxInput(attrs={'class': 'form-check-input'}),
            'dosage_form': TextInput(attrs={'class': 'form-control'}),
            'packing': TextInput(attrs={'class': 'form-control'}),
            'strength': TextInput(attrs={'class': 'form-control'}),
            'batch_number': TextInput(attrs={'class': 'form-control'}),
            'expiry_date': DateInput(attrs={'class': 'form-control'}),
            'prescription_required': CheckboxInput(attrs={'class': 'form-check-input'}),
            'company': Select(attrs={'class': 'form-control', 'data-url': '/company/get-divisions/'}),
            'division': Select(attrs={'class': 'form-control'}),
            'hsn': TextInput(attrs={'class': 'form-control'}),
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
            # Dynamically set choices for the 'gst' field in the __init__ method
            self.fields['gst'].choices = [(gst.id, f"{gst.rate.percentage}%") for gst in GST.objects.all()]

            # Dynamically set choices for the 'company' and 'division' fields in the __init__ method
            self.fields['company'].choices = [(company.id, company.name) for company in Company.objects.all()]
            self.fields['division'].choices = [(division.id, division.name) for division in Division.objects.all()]

            # Set default value for the 'gst' field
            default_gst = GST.objects.select_related('rate').get(rate__percentage=12.0)
            self.fields['gst'].initial = default_gst.id
        except GST.DoesNotExist:
            pass

    def clean_weight(self):
        weight = self.cleaned_data.get('weight')
        if weight is not None and weight < 0:
            raise ValidationError('Weight must be a positive number.')
        return weight