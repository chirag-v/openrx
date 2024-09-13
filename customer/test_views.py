import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from django.test import Client
from customer.models import Customer


@pytest.fixture
def authenticated_client():
    """
    Fixture to create a client with an authenticated user.
    """
    client = Client()
    # Create a test user
    User.objects.create_user(username='testuser', password='password')
    # Log in the test user
    client.login(username='testuser', password='password')
    return client


@pytest.mark.django_db
def test_customer_list_view(authenticated_client):
    client = authenticated_client

    # Create a sample customer to ensure there is data to display
    Customer.objects.create(
        title='Mr.',
        name='Hritik',
        surname='Shah',
        address_line1='123 Main Street, 5th Cross Road',
        mobile='9876543210',
        status='active'
    )

    url = reverse('customer_list')  # Replace with your actual URL name
    response = client.get(url)

    # Ensure the response is successful
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}. Response might be a redirect."

    # Ensure 'page_obj' key is in the context
    assert 'page_obj' in response.context, f"Context keys: {response.context.keys()}"

    # Check if 'page_obj' in the context is a Page instance
    page_obj = response.context['page_obj']
    assert hasattr(page_obj, 'object_list'), "Expected 'page_obj' to have 'object_list' attribute."

    # Ensure there are customers in the page_obj
    assert len(page_obj.object_list) > 0, "No customers found in page_obj."


@pytest.mark.django_db
def test_customer_create_view(authenticated_client):
    client = authenticated_client

    url = reverse('add_customer')  # Replace with your actual URL name
    response = client.post(url, {
        'title': 'Mr.',
        'name': 'Hritik',
        'surname': 'Shah',
        'firm_name': '',
        'type': 'b2c',
        'category': 'bronze',
        'address_line1': '123 Main Street, 5th Cross Road',
        'mobile': '9876543210',
        'status': 'active',
    })

    # Check if the response is a redirect after successful form submission
    assert response.status_code == 302

    # Verify that the customer has been created
    assert Customer.objects.filter(name='Hritik').exists()

    # If the customer is not created, print form errors for debugging
    if not Customer.objects.filter(name='Hritik').exists():
        print(response.context['form'].errors)  # Output form errors for debugging
