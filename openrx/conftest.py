# openrx/tests/conftest.py
import pytest
from django.test import Client
from django.contrib.auth.models import User

@pytest.fixture
def authenticated_client():
    client = Client()
    User.objects.create_user(username='testuser', password='password123')
    client.login(username='testuser', password='password123')
    return client
