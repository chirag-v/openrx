from django import forms
from .models import Supplier


class SupplierForm(forms.ModelForm):
    drug_license1_validity = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    drug_license2_validity = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    food_registration_validity = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    class Meta:
        model = Supplier
        fields = ['name', 'country', 'address_line1', 'address_line2', 'email', 'landmark', 'city', 'pincode', 'phone',
                  'phone2', 'phone3', 'mobile', 'owner_name', 'owner_mobile', 'manager_name', 'manager_mobile',
                  'gst_registration', 'gstin', 'state_code', 'state', 'pan', 'drug_license1', 'drug_license1_validity',
                  'drug_license2', 'drug_license2_validity', 'food_registration', 'food_registration_validity',
                  'status']

    widgets = {
        'name': forms.TextInput(attrs={'id': 'id_name', 'class': 'form-control'}),
        'country': forms.Select(attrs={'id': 'id_country', 'class': 'form-control'}),
        'address_line1': forms.TextInput(attrs={'id': 'id_address_line1', 'class': 'form-control'}),
        'address_line2': forms.TextInput(attrs={'id': 'id_address_line2', 'class': 'form-control'}),
        'email': forms.EmailInput(attrs={'id': 'id_email', 'class': 'form-control'}),
        'landmark': forms.TextInput(attrs={'id': 'id_landmark', 'class': 'form-control'}),
        'city': forms.TextInput(attrs={'id': 'id_city', 'class': 'form-control'}),
        'pincode': forms.TextInput(attrs={'id': 'id_pincode', 'class': 'form-control'}),
        'phone': forms.TextInput(attrs={'id': 'id_phone', 'class': 'form-control'}),
        'phone2': forms.TextInput(attrs={'id': 'id_phone2', 'class': 'form-control'}),
        'phone3': forms.TextInput(attrs={'id': 'id_phone3', 'class': 'form-control'}),
        'mobile': forms.TextInput(attrs={'id': 'id_mobile', 'class': 'form-control'}),
        'owner_name': forms.TextInput(attrs={'id': 'id_owner_name', 'class': 'form-control'}),
        'owner_mobile': forms.TextInput(attrs={'id': 'id_owner_mobile', 'class': 'form-control'}),
        'manager_name': forms.TextInput(attrs={'id': 'id_manager_name', 'class': 'form-control'}),
        'manager_mobile': forms.TextInput(attrs={'id': 'id_manager_mobile', 'class': 'form-control'}),
        'gst_registration': forms.Select(attrs={'id': 'id_gst_registration', 'class': 'form-control'}),
        'gstin': forms.TextInput(attrs={'id': 'id_gstin', 'class': 'form-control'}),
        'state_code': forms.TextInput(attrs={'id': 'id_state_code', 'class': 'form-control'}),
        'state': forms.TextInput(attrs={'id': 'id_state', 'class': 'form-control'}),
        'pan': forms.TextInput(attrs={'id': 'id_pan', 'class': 'form-control'}),
        'drug_license1': forms.TextInput(attrs={'id': 'id_drug_license1', 'class': 'form-control'}),
    }