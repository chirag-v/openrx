import pytest
from customer.models import Customer
from django.core.exceptions import ValidationError

@pytest.mark.django_db
def test_customer_creation():
    # Create a sample customer
    customer = Customer.objects.create(
        title='Mr.',
        name='John',
        surname='Doe',
        firm_name='JD Enterprises',
        address_line1='123 Main Street',
        city='Nagpur',
        pincode='440032',
        phone='1234567890',
        mobile='9876543210',
        type='b2c'
    )
    # Check that the customer has been created successfully
    assert customer.name == 'John'
    assert customer.surname == 'Doe'
    assert customer.firm_name == 'JD Enterprises'

@pytest.mark.django_db
def test_customer_gstin_validator():
    # Test GSTIN validator
    customer = Customer(name='Invalid GST Customer', gstin='INVALIDGSTIN123')
    with pytest.raises(ValidationError):
        customer.full_clean()  # This should raise a ValidationError
