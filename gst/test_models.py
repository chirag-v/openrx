import pytest
from gst.models import GST

@pytest.mark.django_db
def test_gst_model_creation():
    gst = GST.objects.create(percentage=5.0)
    assert GST.objects.count() == 1
    assert gst.percentage == 5.0
    assert str(gst) == "5.0%"

@pytest.mark.django_db
def test_gst_model_unique_percentage():
    GST.objects.create(percentage=5.0)
    with pytest.raises(Exception):  # Replace with specific exception type (e.g., IntegrityError)
        GST.objects.create(percentage=5.0)  # Duplicate percentage should raise an exception
