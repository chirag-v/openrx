# company/forms.py
from django import forms
from django.core.exceptions import ValidationError
from .models import Company, Division, MedicalRepresentative
from django.core.validators import RegexValidator


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'suppliers', 'medical_representative']
        widgets = {
            'supplier': forms.CheckboxSelectMultiple(),
            'medical_representative': forms.Select(),
        }
        help_texts = {
            'medical_representative': 'Select the current medical representative appointed for this company',
        }
        labels = {
            'name': 'Company Name',
            'suppliers': 'Suppliers',
            'medical_representative': 'Medical Representative',
        }


class DivisionForm(forms.ModelForm):
    class Meta:
        model = Division
        fields = ['name', 'company', 'suppliers', 'medical_representative']



class MedicalRepresentativeForm(forms.ModelForm):
    class Meta:
        model = MedicalRepresentative
        fields = ['name', 'mobile_number', 'company', 'division']

    def clean(self):
        cleaned_data = super().clean()
        mobile_number = cleaned_data.get("mobile_number")
        company = cleaned_data.get("company")
        division = cleaned_data.get("division")

        # Define the regex validator for the mobile number
        mobile_validator = RegexValidator(regex=r'^\d{10}$',
                                          message="Mobile number must be exactly 10 digits.")
        # Validate the mobile number
        try:
            mobile_validator(mobile_number)
        except ValidationError as e:
            self.add_error('mobile_number', e)

        if not company and not division:
            raise forms.ValidationError("A Medical Representative must belong to either a company or a division.")

        return cleaned_data