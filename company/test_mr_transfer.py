import pytest
from company import mr_transfer

# company/test_mr_transfer.py

import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from django.test import Client
from company.models import MedicalRepresentative, Company

@pytest.mark.django_db
def test_mr_transfer_success():
    client = Client()

    # Create a user and log them in
    user = User.objects.create_user(username='testuser', password='testpassword')
    client.login(username='testuser', password='testpassword')

    # Create MedicalRepresentative instances
    mr1 = MedicalRepresentative.objects.create(name='John Doe', mobile_number='9876543210')
    mr2 = MedicalRepresentative.objects.create(name='Jane Smith', mobile_number='1234567890')

    # Create a Company instance with the first MedicalRepresentative
    company = Company.objects.create(name='Test Company', medical_representative=mr1)

    # Form data to transfer the MedicalRepresentative
    form_data = {
        'company_id': company.id,
        'new_medical_representative_id': mr2.id
    }

    response = client.post(reverse('mr_transfer'), data=form_data)

    # Check if the response is a redirect
    assert response.status_code == 302

    # Optionally, follow the redirect and check the final response
    response = client.get(response.url)
    assert response.status_code == 200

    # Verify that the MedicalRepresentative has been transferred
    company.refresh_from_db()
    assert company.medical_representative == mr2

def test_mr_transfer_invalid_data():
    # Simulate an invalid transfer operation
    result = mr_transfer(source='source', target='', amount=-50)
    assert result is False
