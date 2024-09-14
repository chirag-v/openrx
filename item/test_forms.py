import pytest
from django.test import override_settings
from item.forms import ItemForm
from gst.models import GST
from company.models import Company, Division

@pytest.mark.django_db
def test_item_form_valid_data():
    gst = GST.objects.create(percentage=12.0)
    company = Company.objects.create(name="Test Company")
    division = Division.objects.create(name="Test Division", company=company)
    form_data = {
        'name': 'Valid Item',
        'item_type': 'medicine',
        'sku': '123456',
        'weight': 10.0,
        'gst': gst.id,
        'company': company.id,
        'division': division.id
    }
    form = ItemForm(data=form_data)
    assert form.is_valid(), f"Form errors: {form.errors}"

@pytest.mark.django_db
@override_settings(DEBUG=True)
def test_item_form_invalid_data():
    form_data = {
        'name': '',  # Missing required name
        'item_type': 'invalid_type',  # Invalid choice for item_type
        'sku': 'invalid_sku!',  # Invalid SKU format
        'weight': -10,  # Invalid weight (negative value)
    }
    form = ItemForm(data=form_data)
    assert not form.is_valid()
    assert 'name' in form.errors
    assert 'item_type' in form.errors
    assert 'sku' in form.errors
    assert 'weight' in form.errors