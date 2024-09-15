# tests/test_views.py

import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from django.test import Client

@pytest.mark.django_db
class TestGSTView:

    def setup_method(self):
        # Setup initial data
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')  # Authenticate the test client

    def test_gst_view_access(self):
        url = reverse('gst_view')
        response = self.client.get(url)

        assert response.status_code == 200
        assert 'gst/gst_coming_soon.html' in [t.name for t in response.templates]
        assert 'GSTR-1 Utility (Coming Soon)' in response.content.decode('utf-8')
