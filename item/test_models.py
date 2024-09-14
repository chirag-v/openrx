import pytest
from item.models import Item
from gst.models import GST
from company.models import Company, Division

@pytest.mark.django_db
def test_item_model_creation():
    gst = GST.objects.create(percentage=12.0)
    company = Company.objects.create(name="Test Company")
    division = Division.objects.create(name="Test Division", company=company)
    item = Item.objects.create(
        name='Test Item',
        item_type='medicine',
        sku='1234567890',
        weight=10.0,
        gst=gst,
        company=company,
        division=division
    )
    assert Item.objects.count() == 1
    assert item.name == 'Test Item'
    assert item.item_type == 'medicine'
    assert item.gst.percentage == 12.0
    assert str(item) == 'Test Item'

@pytest.mark.django_db
def test_item_model_unique_sku():
    gst = GST.objects.create(percentage=5.0)
    company = Company.objects.create(name="Another Company")
    Item.objects.create(name='Item 1', sku='1111111111', weight=5.0, gst=gst, company=company)
    with pytest.raises(Exception):  # Replace with specific exception type (e.g., IntegrityError)
        Item.objects.create(name='Item 2', sku='1111111111', weight=5.0, gst=gst, company=company)  # Duplicate SKU should raise an exception
