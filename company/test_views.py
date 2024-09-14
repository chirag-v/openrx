# company/test_views.py

import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from django.test import Client
from company.models import Company, MedicalRepresentative

@pytest.fixture
def authenticated_client():
    client = Client()
    User.objects.create_user(username='testuser', password='password')
    client.login(username='testuser', password='password')
    return client

@pytest.mark.django_db
def test_company_list_view(authenticated_client):
    client = authenticated_client
    Company.objects.create(name='Test Company')
    url = reverse('company_list')
    response = client.get(url)
    assert response.status_code == 200
    assert 'page_obj' in response.context


@pytest.mark.django_db
def test_add_company_view():
    client = Client()

    # Create a user and log them in
    user = User.objects.create_user(username='testuser', password='testpassword')
    client.login(username='testuser', password='testpassword')

    # Create a MedicalRepresentative instance
    medical_representative = MedicalRepresentative.objects.create(name='John Doe', mobile_number='9876543210')

    # Form data with valid medical representative ID
    form_data = {
        'name': 'Test Company',
        'medical_representative': medical_representative.id
    }

    response = client.post(reverse('add_company'), data=form_data)

    # Check if the response is a redirect
    assert response.status_code == 302

    # Optionally, follow the redirect and check the final response
    response = client.get(response.url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_delete_company_view(authenticated_client):
    client = authenticated_client
    company = Company.objects.create(name='To Be Deleted')
    url = reverse('delete_company', args=[company.id])
    response = client.post(url)
    assert response.status_code == 302
    assert not Company.objects.filter(id=company.id).exists()
