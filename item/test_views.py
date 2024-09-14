import pytest
from django.urls import reverse
from django.test import Client
from django.contrib.auth.models import User
from item.models import Item
from gst.models import GST
from company.models import Company, Division


@pytest.fixture
def authenticated_client():
    client = Client()
    User.objects.create_user(username='testuser', password='password')
    client.login(username='testuser', password='password')
    return client


@pytest.mark.django_db
def test_create_item_view(authenticated_client):
    gst = GST.objects.create(percentage=12.0)
    company = Company.objects.create(name="Test Company")
    division = Division.objects.create(name="Test Division", company=company)

    url = reverse('create_item')
    response = authenticated_client.post(url, {
        'name': 'New Item',
        'item_type': 'medicine',
        'sku': '123456',
        'weight': 10.0,
        'gst': gst.id,
        'company': company.id,
        'division': division.id
    })
    assert response.status_code == 302  # Should redirect after successful creation
    assert Item.objects.count() == 1


@pytest.mark.django_db
def test_item_list_view(authenticated_client):
    url = reverse('item_list')
    response = authenticated_client.get(url)
    assert response.status_code == 200
    assert 'page_obj' in response.context


@pytest.mark.django_db
def test_edit_item_view(authenticated_client):
    gst = GST.objects.create(percentage=12.0)
    company = Company.objects.create(name="Test Company")
    division = Division.objects.create(name="Test Division", company=company)
    item = Item.objects.create(name='Editable Item', sku='123456', weight=10.0, gst=gst, company=company,
                               division=division)

    url = reverse('edit_item', kwargs={'pk': item.pk})
    response = authenticated_client.post(url, {'name': 'Updated Item', 'item_type': 'medicine', 'sku': '123456',
                                               'weight': 15.0, 'gst': gst.id, 'company': company.id,
                                               'division': division.id})
    assert response.status_code == 302  # Should redirect after successful edit
    item.refresh_from_db()
    assert item.name == 'Updated Item'
    assert item.weight == 15.0


@pytest.mark.django_db
def test_delete_item_view(authenticated_client):
    gst = GST.objects.create(percentage=12.0)
    company = Company.objects.create(name="Test Company")
    division = Division.objects.create(name="Test Division", company=company)
    item = Item.objects.create(name='Deletable Item', sku='123456', weight=10.0, gst=gst, company=company,
                               division=division)

    url = reverse('delete_item', kwargs={'pk': item.pk})
    response = authenticated_client.post(url)
    assert response.status_code == 302  # Should redirect after deletion
    assert Item.objects.count() == 0


@pytest.mark.django_db
def test_get_item_gst_view(authenticated_client):
    gst = GST.objects.create(percentage=12.0)
    item = Item.objects.create(name='GST Item', sku='123456', weight=10.0, gst=gst)
    url = reverse('get_item_gst', kwargs={'item_id': item.id})
    response = authenticated_client.get(url)
    assert response.status_code == 200
    assert response.json() == {'gst': 12.0}


@pytest.mark.django_db
def test_get_items_view(authenticated_client):
    Item.objects.create(name='Item 1', sku='123456', weight=10.0, gst=GST.objects.create(percentage=12.0))
    url = reverse('get_items')
    response = authenticated_client.get(url)
    assert response.status_code == 200
    assert 'items' in response.json()
    assert len(response.json()['items']) == 1
