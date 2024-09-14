# purchase/tests/test_views.py
import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from django.test import Client

from purchase.models import Purchase
from supplier.models import Supplier


@pytest.fixture
def authenticated_client():
    client = Client()
    User.objects.create_user(username='testuser', password='password123')
    client.login(username='testuser', password='password123')
    return client


@pytest.mark.django_db
def test_create_purchase_view(authenticated_client):
    client = authenticated_client
    supplier = Supplier.objects.create(name="Test Supplier")
    url = reverse('create_purchase')
    response = client.post(url, {
        'supplier_name': supplier.id,
        'purchase_type': 'cash',
        'invoice_number': 'INV123',
        'invoice_date': '2023-09-14',
        'invoice_discount': 10.0,
    })
    assert response.status_code == 200 or response.status_code == 302  # Adjust based on expected outcome


@pytest.mark.django_db
def test_purchase_list_view(authenticated_client):
    client = authenticated_client
    url = reverse('purchase_list')
    response = client.get(url)
    assert response.status_code == 200
    assert 'page_obj' in response.context


@pytest.mark.django_db
def test_edit_purchase_view(authenticated_client):
    client = authenticated_client
    supplier = Supplier.objects.create(name="Test Supplier")
    purchase = Purchase.objects.create(
        supplier_name=supplier,
        purchase_type='cash',
        invoice_number='INV123',
        invoice_date='2023-09-14',
        invoice_discount=10.0
    )
    url = reverse('edit_purchase', args=[purchase.id])
    response = client.post(url, {
        'supplier_name': supplier.id,
        'purchase_type': 'cash',
        'invoice_number': 'INV124',  # Changed invoice number
        'invoice_date': '2023-09-15',
        'invoice_discount': 5.0,
    })
    assert response.status_code == 200 or response.status_code == 302  # Adjust based on expected outcome
