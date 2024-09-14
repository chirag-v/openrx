# company/test_models.py

import pytest
from company.models import Company, MedicalRepresentative

@pytest.mark.django_db
def test_create_company():
    # Create a MedicalRepresentative instance
    medical_representative = MedicalRepresentative.objects.create(name='John Doe', mobile_number='9876543210')

    # Create a Company instance with the MedicalRepresentative instance
    company = Company.objects.create(
        name='Test Company',
        medical_representative=medical_representative
    )

    assert company.name == 'Test Company'
    assert company.medical_representative == medical_representative
@pytest.mark.django_db
def test_create_medical_representative():
    representative = MedicalRepresentative.objects.create(
        name='John Doe',
        mobile_number='9876543210'
    )
    assert MedicalRepresentative.objects.count() == 1
    assert representative.name == 'John Doe'
