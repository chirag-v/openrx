# supplier/tests/test_models.py
import pytest
from supplier.models import Supplier
from datetime import date

@pytest.mark.django_db
def test_supplier_model_creation():
    supplier = Supplier.objects.create(
        name='Test Supplier',
        country='India',
        address_line1='123 Street',
        city='New Delhi',
        pincode='110011',
        phone='9876543210',
        mobile='9876543210',
        owner_name='Owner Name',
        gst_registration='registered',
        gstin='07ABCDE1234F2Z5',  # Valid GSTIN
        drug_license1='DL123',
        drug_license1_validity=date.today(),
        status='active'
    )
    assert supplier.id is not None
    assert supplier.state.lower() == 'delhi'.lower()  # Normalize case for comparison