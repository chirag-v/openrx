# openrx/tests/test_views.py
import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from django.test import Client


@pytest.mark.django_db
def test_homepage_view(authenticated_client):
    client = authenticated_client
    url = reverse('homepage')
    response = client.get(url)

    assert response.status_code == 200
    assert 'apps_and_features' in response.context


@pytest.mark.django_db
def test_login_view(client):
    url = reverse('login')
    response = client.post(url, {'username': 'testuser', 'password': 'password123'})

    assert response.status_code == 200
    assert 'form' in response.context
    assert response.context['form'].is_valid() is False


@pytest.mark.django_db
def test_logout_view(authenticated_client):
    client = authenticated_client
    url = reverse('logout')
    response = client.get(url)

    assert response.status_code == 302
    assert response.url == reverse('login')


@pytest.mark.django_db
def test_search_view(authenticated_client):
    client = authenticated_client
    url = reverse('search')
    response = client.get(url, {'q': 'test'})

    assert response.status_code == 200
    assert 'results' in response.json()
