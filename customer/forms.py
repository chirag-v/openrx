from django import forms
from .models import Customer
from gst.validators import gstin_validator

class CustomerForm(forms.ModelForm):
    gstin = forms.CharField(validators=[gstin_validator], required=False)  # Applying validator to gstin field

    class Meta:
        model = Customer
        fields = [
            'title', 'name', 'surname', 'firm_name', 'address_line1', 'address_line2',
            'email', 'landmark', 'city', 'pincode', 'phone', 'mobile', 'type',
            'category', 'gst_registration', 'gstin', 'state_code', 'state', 'pan', 'current_status'
        ]

        widgets = {
            'title': forms.Select(attrs={'id': 'id_title'}, choices=Customer.TITLE_CHOICES),
            'type': forms.RadioSelect(attrs={'class': 'type-radio'}, choices=Customer.TYPE_CHOICES),
            'category': forms.Select(choices=Customer.CATEGORY_CHOICES),
            'gst_registration': forms.Select(choices=Customer.GST_REGISTRATION_CHOICES),
            'current_status': forms.Select(choices=Customer.CURRENT_STATUS_CHOICES),
            'gstin': forms.TextInput(attrs={'maxlength': 15, 'required': False}),
            'name': forms.TextInput(attrs={'id': 'id_name', 'class': 'form-control'}),
            'surname': forms.TextInput(attrs={'id': 'id_surname', 'class': 'form-control'}),
            'firm_name': forms.TextInput(attrs={'id': 'id_firm_name', 'class': 'form-control'}),
            'pincode': forms.TextInput(attrs={'maxlength': 6}),
            'phone': forms.TextInput(attrs={'maxlength': 20}),
            'mobile': forms.TextInput(attrs={'maxlength': 10}),
            'state_code': forms.TextInput(attrs={'id': 'id_state_code'}),
            'state': forms.TextInput(attrs={'id': 'id_state', 'class': 'form-control'}),
            'pan': forms.TextInput(attrs={'id': 'id_pan'}),
        }

    def __init__(self, *args, **kwargs):
        super(CustomerForm, self).__init__(*args, **kwargs)
        self.fields['gstin'].required = False

    def clean(self):
        cleaned_data = super().clean()
        type = cleaned_data.get("type")
        title = cleaned_data.get("title")
        name = cleaned_data.get("name")
        surname = cleaned_data.get("surname")
        firm_name = cleaned_data.get("firm_name")
        category = cleaned_data.get("category")

        if type == 'b2c':
            if title == 'M/s':
                self.add_error('title', 'Title cannot be Messrs for B2C customers.')
            if not name or not surname:
                self.add_error('name', 'Name and surname are mandatory for B2C customers.')
                self.add_error('surname', 'Name and surname are mandatory for B2C customers.')
            if firm_name:
                self.add_error('firm_name', 'Firm name must be empty for B2C customers.')
        elif type == 'b2b':
            if title in ['Mr.', 'Mrs.', 'Miss', 'Master', 'Adv.', 'Dr.', 'Prof.']:
                self.add_error('title', 'Title cannot be Mr, Mrs, Miss, Master, Adv, Dr, or Prof for B2B customers.')
            if not firm_name:
                self.add_error('firm_name', 'Firm name is mandatory for B2B customers.')
            if name or surname:
                self.add_error('name', 'Name and surname must be empty for B2B customers.')
                self.add_error('surname', 'Name and surname must be empty for B2B customers.')

        if type == 'b2b' and category not in ['wholesaler', 'retailer', 'superstockist', 'not applicable']:
            self.add_error('category', 'Invalid category for B2B type.')
        elif type == 'b2c' and category not in ['bronze', 'silver', 'gold', 'platinum', 'not applicable']:
            self.add_error('category', 'Invalid category for B2C type.')

        return cleaned_data