import pytest
from customer.forms import CustomerForm

@pytest.mark.django_db
def test_customer_form_valid_data():
    form_data = {
        'title': 'Mr.',
        'name': 'John',
        'surname': 'Doe',
        'firm_name': '',
        'type': 'b2c',
        'category': 'bronze',
        'address_line1': '123 Main Street',
        'mobile': '9876543210',
        'status': 'active',  # Adjust based on the actual choices
    }
    form = CustomerForm(data=form_data)
    assert form.is_valid()

@pytest.mark.django_db
def test_customer_form_invalid_title_for_b2b():
    # This form data is intended to be invalid because it has 'name' and 'surname' for a b2b customer
    form_data = {
        'title': 'Mr.',  # Invalid title for b2b customer type
        'name': 'John',  # Invalid field for b2b customer type
        'surname': 'Doe',  # Invalid field for b2b customer type
        'firm_name': '',  # Missing firm_name for b2b customer type
        'type': 'b2b',
        'category': 'wholesaler',
        'address_line1': '123 Main Street',
        'mobile': '9876543210',
        'status': 'active',
        'gstin': '29ABCDE1234F2Z5',  # Assuming this is a valid format
    }

    form = CustomerForm(data=form_data)

    # Form should be invalid due to improper fields for b2b type
    assert not form.is_valid()

    # Ensure specific errors are raised
    assert 'title' in form.errors  # The title should be invalid for b2b customers
    assert 'name' in form.errors  # Name should not exist for b2b customers
    assert 'surname' in form.errors  # Surname should not exist for b2b customers
    assert 'firm_name' in form.errors  # firm_name is required for b2b customers


@pytest.mark.django_db
def test_customer_form_invalid_category_for_b2c():
    form_data = {
        'title': 'Miss',
        'name': 'Jane',
        'surname': 'Doe',
        'type': 'b2c',
        'category': 'invalid_category'
    }
    form = CustomerForm(data=form_data)
    assert not form.is_valid()
    assert 'category' in form.errors
