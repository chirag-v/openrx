# purchase/tests/test_forms.py
import pytest
from django.urls import reverse
from django.test import Client
from django.contrib.auth.models import User
from supplier.models import Supplier
from item.models import Item
from gst.models import GST
from purchase.models import Purchase, PurchaseItem

@pytest.mark.django_db
def test_purchase_and_purchase_item_forms():
    client = Client()
    user = User.objects.create_user(username='testuser', password='testpassword')
    client.login(username='testuser', password='testpassword')

    supplier = Supplier.objects.create(name="Test Supplier")
    gst = GST.objects.create(percentage=18)
    item = Item.objects.create(name="Test Item", weight=1.0, gst=gst)

    purchase_form_data = {
        'supplier_name': supplier.id,
        'purchase_type': 'cash',
        'invoice_number': 'INV123',
        'invoice_date': '2023-09-14',
        'invoice_discount': 10.0,
    }

    purchase_item_form_data = {
        'form-TOTAL_FORMS': '1',
        'form-INITIAL_FORMS': '0',
        'form-MIN_NUM_FORMS': '0',
        'form-MAX_NUM_FORMS': '1000',
        'form-0-item': item.id,
        'form-0-mrp': 100.0,
        'form-0-quantity': 10,
        'form-0-free': 0,
        'form-0-batch_number': 'BATCH123',
        'form-0-expiry_date': '12/23',
        'form-0-purchase_rate': 80.0,
        'form-0-item_discount_percentage': 5.0,
        'form-0-item_discount_amount': 4.0,
    }

    url = reverse('create_purchase')
    response = client.post(url, {**purchase_form_data, **purchase_item_form_data})

    assert response.status_code == 200 or response.status_code == 302

    purchase = Purchase.objects.get(invoice_number='INV123')
    assert purchase is not None
    assert purchase.supplier_name == supplier

    purchase_item = PurchaseItem.objects.get(purchase=purchase)
    assert purchase_item is not None
    assert purchase_item.item == item
    assert purchase_item.quantity == 10

@pytest.mark.django_db
def test_purchase_form_data_incorrect():
    client = Client()
    user = User.objects.create_user(username='testuser', password='testpassword')
    client.login(username='testuser', password='testpassword')

    supplier = Supplier.objects.create(name="Test Supplier")
    gst = GST.objects.create(percentage=18)
    item = Item.objects.create(name="Test Item", weight=1.0, gst=gst)

    purchase_form_data = {
        'supplier_name': supplier.id,
        'purchase_type': 'cash',
        'invoice_date': '2023-09-14',
        'invoice_discount': 10.0,
    }

    purchase_item_form_data = {
        'form-TOTAL_FORMS': '1',
        'form-INITIAL_FORMS': '0',
        'form-MIN_NUM_FORMS': '0',
        'form-MAX_NUM_FORMS': '1000',
        'form-0-item': item.id,
        'form-0-mrp': 100.0,
        'form-0-quantity': 10,
        'form-0-free': 0,
        'form-0-batch_number': 'BATCH123',
        'form-0-expiry_date': '12/23',
        'form-0-purchase_rate': 80.0,
        'form-0-item_discount_percentage': 5.0,
        'form-0-item_discount_amount': 4.0,
    }

    url = reverse('create_purchase')
    response = client.post(url, {**purchase_form_data, **purchase_item_form_data})

    assert response.status_code == 200

    # Print context keys to debug
    print(response.context.keys())

    # Check for the correct form name
    assert 'invoice_number' in response.context['form'].errors


@pytest.mark.django_db
def test_purchase_item_form_data_incorrect():
    client = Client()
    user = User.objects.create_user(username='testuser', password='testpassword')
    client.login(username='testuser', password='testpassword')

    supplier = Supplier.objects.create(name="Test Supplier")
    gst = GST.objects.create(percentage=18)
    item = Item.objects.create(name="Test Item", weight=1.0, gst=gst)

    purchase_form_data = {
        'supplier_name': supplier.id,
        'purchase_type': 'cash',
        'invoice_number': 'INV123',
        'invoice_date': '2023-09-14',
        'invoice_discount': 10.0,
    }

    purchase_item_form_data = {
        'form-TOTAL_FORMS': '1',
        'form-INITIAL_FORMS': '0',
        'form-MIN_NUM_FORMS': '0',
        'form-MAX_NUM_FORMS': '1000',
        'form-0-mrp': 100.0,
        'form-0-quantity': 10,
        'form-0-free': 0,
        'form-0-batch_number': 'BATCH123',
        'form-0-expiry_date': '12/23',
        'form-0-purchase_rate': 80.0,
        'form-0-item_discount_percentage': 5.0,
        'form-0-item_discount_amount': 4.0,
    }

    url = reverse('create_purchase')
    response = client.post(url, {**purchase_form_data, **purchase_item_form_data})

    assert response.status_code == 200

    # Print context keys to debug
    print(response.context.keys())

    # Check for the correct formset name
    assert 'item' in response.context['formset'].forms[0].errors