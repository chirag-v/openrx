# openrx/tests/test_middleware.py
import pytest
from django.test import RequestFactory
from django.urls import reverse
from openrx.middleware import LoginRequiredMiddleware
from django.contrib.auth.models import AnonymousUser, User


@pytest.mark.django_db
def test_middleware_redirects_unauthenticated_user():
    factory = RequestFactory()
    request = factory.get(reverse('homepage'))
    request.user = AnonymousUser()
    middleware = LoginRequiredMiddleware(lambda req: None)
    response = middleware(request)

    assert response.status_code == 302
    assert response.url == reverse('login')


@pytest.mark.django_db
def test_middleware_allows_authenticated_user():
    factory = RequestFactory()
    request = factory.get(reverse('homepage'))
    request.user = User.objects.create_user(username='testuser', password='password123')
    middleware = LoginRequiredMiddleware(lambda req: None)
    response = middleware(request)

    assert response is None  # No redirect, as user is authenticated
