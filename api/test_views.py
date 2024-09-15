# tests/test_views.py

import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient
from company.models import MedicalRepresentative, Division, Company
from gst.models import StateCode

@pytest.mark.django_db
class TestMedicalRepresentativeInfoView:

    def setup_method(self):
        # Setup initial data
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')  # Authenticate the test client

        self.company = Company.objects.create(name="Test Company")
        self.division = Division.objects.create(name="Test Division", company=self.company)
        self.med_rep = MedicalRepresentative.objects.create(name="Test Rep", division=self.division)

    def test_get_medical_representative_info_success(self):
        url = reverse('api:medical_representative_info')
        response = self.client.get(url, {'med_rep_id': self.med_rep.id})

        assert response.status_code == status.HTTP_200_OK
        assert response.data['company'] == self.company.name
        assert response.data['division'] == self.division.name
        assert response.data['division_id'] == str(self.division.id)

    def test_get_medical_representative_info_not_found(self):
        url = reverse('api:medical_representative_info')
        response = self.client.get(url, {'med_rep_id': 9999})  # Assuming this ID does not exist

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert 'error' in response.data

    def test_get_medical_representative_info_missing_param(self):
        url = reverse('api:medical_representative_info')
        response = self.client.get(url)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'error' in response.data


@pytest.mark.django_db
class TestGetStateNameView:

    def setup_method(self):
        # Setup initial data
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')  # Authenticate the test client

        self.state_code = StateCode.objects.create(code="MH", name="Maharashtra")

    def test_get_state_name_success(self):
        url = reverse('api:get_state_name')
        response = self.client.get(url, {'code': self.state_code.code})

        assert response.status_code == status.HTTP_200_OK
        assert response.json()['stateName'] == self.state_code.name

    def test_get_state_name_not_found(self):
        url = reverse('api:get_state_name')
        response = self.client.get(url, {'code': 'XX'})  # Assuming this code does not exist

        assert response.status_code == status.HTTP_200_OK
        assert response.json()['stateName'] == ''
