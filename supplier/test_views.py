# supplier/tests/test_views.py
import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from django.test import Client
from supplier.models import Supplier
from datetime import date


@pytest.fixture
def authenticated_client():
    client = Client()
    User.objects.create_user(username='testuser', password='password123')
    client.login(username='testuser', password='password123')
    return client


@pytest.mark.django_db
def test_supplier_list_view(authenticated_client):
    client = authenticated_client
    url = reverse('supplier_list')
    response = client.get(url)
    assert response.status_code == 200
    assert 'page_obj' in response.context


@pytest.fixture
def authenticated_client():
    client = Client()
    User.objects.create_user(username='testuser', password='password123')
    client.login(username='testuser', password='password123')
    return client

@pytest.mark.django_db
def test_add_supplier_view(authenticated_client):
    client = authenticated_client
    url = reverse('add_supplier')
    response = client.post(url, {
        'name': 'New Supplier',
        'country': 'India',
        'address_line1': '456 Street',
        'city': 'Mumbai',
        'pincode': '400001',
        'phone': '9876543211',
        'mobile': '9876543212',
        'owner_name': 'New Owner',
        'gst_registration': 'registered',
        'gstin': '27ABCDE1234F2Z5',  # Valid GSTIN
        'drug_license1': 'DL456',
        'drug_license1_validity': date.today(),
        'drug_license2': 'DL789',
        'drug_license2_validity': date.today(),
        'food_registration': 'FR456',
        'food_registration_validity': date.today(),
        'status': 'active'
    })
    assert response.status_code == 302, response.content  # Print response content if status code is not 302

@pytest.mark.django_db
def test_edit_supplier_view(authenticated_client):
    client = authenticated_client
    supplier = Supplier.objects.create(
        name='Edit Supplier',
        country='India',
        address_line1='789 Street',
        city='Bangalore',
        pincode='560001',
        phone='9876543213',
        gstin='29ABCDE1234F2Z5',
    )
    url = reverse('edit_supplier', args=[supplier.id])
    response = client.post(url, {
        'name': 'Updated Supplier',
        'country': 'India',
        'address_line1': '789 Street Updated',
        'city': 'Bangalore',
        'pincode': '560001',
        'phone': '9876543214',
        'gstin': '29ABCDE1234F2Z5',
        'drug_license1': 'DL456',
        'drug_license1_validity': date.today(),
        'drug_license2': 'DL789',
        'drug_license2_validity': date.today(),
        'food_registration': 'FR456',
        'food_registration_validity': date.today(),
        'status': 'active'
    })
    assert response.status_code == 302, response.content  # Print response content if status code is not 302

@pytest.mark.django_db
def test_delete_supplier_view(authenticated_client):
    client = authenticated_client
    supplier = Supplier.objects.create(name='Delete Supplier')
    url = reverse('delete_supplier', args=[supplier.id])
    response = client.post(url)
    assert response.status_code == 302  # Should redirect after successful deletion


@pytest.mark.django_db
def test_get_gstin_view(authenticated_client):
    client = authenticated_client
    supplier = Supplier.objects.create(name='Supplier with GST', gstin='27ABCDE1234F2Z5')
    url = reverse('get_gstin', args=[supplier.id])
    response = client.get(url)
    assert response.status_code == 200
    assert response.json() == {'gstin': '27ABCDE1234F2Z5'}
