# company/test_forms.py

import pytest
from company.forms import CompanyForm, MedicalRepresentativeForm
from company.models import Supplier, Company, Division


@pytest.mark.django_db
def test_company_form_valid_data():
    # Create Supplier objects
    supplier1 = Supplier.objects.create(name='Supplier 1')
    supplier2 = Supplier.objects.create(name='Supplier 2')

    # Form data with valid supplier IDs
    form_data = {
        'name': 'Test Company',
        'address': '123 Test St',
        'suppliers': [supplier1.id, supplier2.id],  # Use valid supplier IDs
    }
    form = CompanyForm(data=form_data)
    assert form.is_valid(), f"Form errors: {form.errors}"

@pytest.mark.django_db
def test_company_form_invalid_data():
    form_data = {
        'name': '',  # Invalid: Name is required
        'suppliers': [],
        'medical_representative': ''
    }
    form = CompanyForm(data=form_data)
    assert not form.is_valid()
    assert 'name' in form.errors

@pytest.mark.django_db
def test_medical_representative_form_valid_data():
    company = Company.objects.create(name='Sigma Labs')
    division = Division.objects.create(name='Derma', company=company)

    form_data = {
        'name': 'Sanjay Sharma',
        'mobile_number': '9876543210',
        'company': company.id,
        'division': division.id
    }
    form = MedicalRepresentativeForm(data=form_data)
    assert form.is_valid(), f"Form errors: {form.errors}"

@pytest.mark.django_db
def test_medical_representative_form_invalid_data():
    form_data = {
        'name': '',  # Invalid: Name is required
        'mobile_number': '123'  # Invalid: Mobile number should be valid
    }
    form = MedicalRepresentativeForm(data=form_data)
    assert not form.is_valid()
    assert 'name' in form.errors
    assert 'mobile_number' in form.errors
