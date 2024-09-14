# purchase/tests/test_models.py
import pytest
from purchase.models import Purchase, PurchaseItem
from item.models import Item
from supplier.models import Supplier
from gst.models import GST




@pytest.mark.django_db
def test_purchase_model_creation():
    supplier = Supplier.objects.create(name="Test Supplier")
    purchase = Purchase.objects.create(
        supplier_name=supplier,
        purchase_type='cash',
        invoice_number='INV123',
        invoice_date='2023-09-14',
        invoice_discount=10.0
    )
    assert purchase.id is not None
    assert str(purchase) == f"Purchase INV123 from {supplier}"

@pytest.mark.django_db
def test_purchase_item_model_calculate_amount():
    supplier = Supplier.objects.create(name="Test Supplier")
    gst = GST.objects.create(percentage=18)
    item = Item.objects.create(name="Test Item", weight=1.0, gst=gst)  # Added gst
    purchase = Purchase.objects.create(
        supplier_name=supplier,
        purchase_type='cash',
        invoice_number='INV123',
        invoice_date='2023-09-14',
        invoice_discount=10.0
    )
    purchase_item = PurchaseItem.objects.create(
        purchase=purchase,
        item=item,
        mrp=100.0,
        quantity=10,
        free=0,
        batch_number='BATCH123',
        expiry_date='2023-12-31',
        purchase_rate=80.0,
        item_discount_percentage=5.0,
        item_discount_amount=4.0
    )
    purchase_item.calculate_amount()
    assert purchase_item.amount > 0