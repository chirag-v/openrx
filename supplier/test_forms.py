# supplier/tests/test_forms.py
import pytest
from datetime import date
from supplier.forms import SupplierForm

@pytest.mark.django_db
def test_supplier_form_valid_data():
    form_data = {
        'name': 'Test Supplier',
        'country': 'India',
        'address_line1': '123 Street',
        'city': 'New Delhi',
        'pincode': '110011',
        'phone': '9876543210',
        'mobile': '9876543210',
        'owner_name': 'Owner Name',
        'owner_mobile': '9876543210',
        'gst_registration': 'registered',
        'gstin': '07ABCDE1234F2Z5',
        'state_code': '07',
        'state': 'Delhi',
        'drug_license1': 'DL123',
        'drug_license1_validity': date.today(),
        'drug_license2': 'DL456',
        'drug_license2_validity': date.today(),
        'food_registration': 'FR123',
        'food_registration_validity': date.today(),
        'status': 'active'
    }
    form = SupplierForm(data=form_data)
    assert form.is_valid(), form.errors  # Print form errors if invalid

@pytest.mark.django_db
def test_supplier_form_invalid_data():
    form_data = {
        'name': '',  # Missing name
        'country': '',
        'address_line1': '',
        'city': '',
        'pincode': 'invalid_pincode',  # Invalid pincode
        'phone': 'invalid_phone',  # Invalid phone
        'gstin': 'invalid_gstin',  # Invalid GSTIN
    }
    form = SupplierForm(data=form_data)
    assert not form.is_valid()
    assert 'name' in form.errors
    assert 'pincode' in form.errors
    assert 'phone' in form.errors
    assert 'gstin' in form.errors
