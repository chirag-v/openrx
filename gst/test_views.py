import pytest
from django.urls import reverse
from django.test import Client
from django.contrib.auth.models import User
from unittest.mock import patch


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
def test_get_state_name_view(authenticated_client):
    # Mock the function that fetches the state name from the code
    with patch('gst.utils.get_state_name_by_code', return_value='Maharashtra'):
        url = reverse('get_state_name')
        response = authenticated_client.get(url, {'code': '27'})  # Assuming '27' corresponds to 'Maharashtra'
        assert response.status_code == 200

        # Normalize to title case for comparison
        actual_state_name = response.json()['stateName'].title()
        expected_state_name = 'Maharashtra'.title()
        assert actual_state_name == expected_state_name


@pytest.mark.django_db
def test_get_state_name_view_invalid_code(authenticated_client):
    # Mock the function to return 'CENTRE JURISDICTION' for an invalid code
    with patch('gst.utils.get_state_name_by_code', return_value='CENTRE JURISDICTION'):
        url = reverse('get_state_name')
        response = authenticated_client.get(url, {'code': '99'})  # Assuming '99' is an invalid code
        assert response.status_code == 200
        assert response.json() == {'stateName': 'CENTRE JURISDICTION'}
