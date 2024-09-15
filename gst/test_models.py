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


# tests/test_models.py

import pytest
from gst.models import GST, StateCode


@pytest.mark.django_db
class TestGSTModel:

    def test_create_gst(self):
        # Test creating a GST entry
        gst_entry = GST.objects.create(percentage=18.0)
        assert gst_entry.percentage == 18.0
        assert str(gst_entry) == "18.0%"

    def test_unique_gst_percentage(self):
        # Test unique constraint on percentage field
        GST.objects.create(percentage=5.0)
        with pytest.raises(Exception):
            GST.objects.create(percentage=5.0)  # This should raise an integrity error due to uniqueness


@pytest.mark.django_db
class TestStateCodeModel:

    def test_create_state_code(self):
        # Test creating a StateCode entry
        state_code = StateCode.objects.create(code='MH', name='Maharashtra')
        assert state_code.code == 'MH'
        assert state_code.name == 'Maharashtra'
        assert str(state_code) == "MH - Maharashtra"

    def test_unique_state_code(self):
        # Test unique constraint on the code field
        StateCode.objects.create(code='KA', name='Karnataka')
        with pytest.raises(Exception):
            StateCode.objects.create(code='KA', name='Kerala')  # This should raise an integrity error due to uniqueness
