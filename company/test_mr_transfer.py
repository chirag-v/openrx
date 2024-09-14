# company/test_mr_transfer.py

from company import mr_transfer
import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from django.test import Client
from company.models import Company, Division, MedicalRepresentative
from company.views import logger


@pytest.fixture
def client():
    return Client()

@pytest.fixture
def user(db):
    return User.objects.create_user(username='testuser', password='testpassword')

def test_mr_transfer_success(client, user):
    client.login(username='testuser', password='testpassword')

    # Assuming you have the necessary setup for medical representatives, companies, and divisions
    response = client.post(reverse('mr_transfer'), {
        'med_rep_id': 1,
        'leaving_division_id': 1,
        'joining_division_id': 2,
        'joining_company_id': 1
    })

    assert response.status_code == 200

@pytest.fixture
def client():
    return Client()

@pytest.fixture
def user(db):
    return User.objects.create_user(username='testuser', password='testpassword')

@pytest.mark.django_db
def test_mr_transfer_success(client, user):
    client.login(username='testuser', password='testpassword')

    # Create necessary objects
    company = Company.objects.create(name='Test Company')
    division1 = Division.objects.create(name='Division 1', company=company)
    division2 = Division.objects.create(name='Division 2', company=company)
    med_rep = MedicalRepresentative.objects.create(name='John Doe', company=company)

    # Valid data
    response = client.post(reverse('mr_transfer'), {
        'med_rep_id': med_rep.id,
        'leaving_division_id': division1.id,
        'joining_division_id': division2.id,
        'joining_company_id': company.id
    })

    assert response.status_code == 302  # Assuming a redirect on success


@pytest.fixture
def client():
    return Client()

@pytest.fixture
def user(db):
    return User.objects.create_user(username='testuser', password='testpassword')

@pytest.mark.django_db
def test_mr_transfer_success(client, user):
    client.login(username='testuser', password='testpassword')

    # Create necessary objects
    company = Company.objects.create(name='Test Company')
    division1 = Division.objects.create(name='Division 1', company=company)
    division2 = Division.objects.create(name='Division 2', company=company)
    med_rep = MedicalRepresentative.objects.create(name='John Doe', company=company)

    # Assign the Medical Representative to the leaving division
    med_rep.division = division1
    med_rep.save()


    # Valid data
    response = client.post(reverse('mr_transfer'), {
        'med_rep_id': med_rep.id,
        'leaving_division_id': division1.id,
        'joining_division_id': division2.id,
        'joining_company_id': company.id
    })

    assert response.status_code == 302  # Assuming a redirect on success