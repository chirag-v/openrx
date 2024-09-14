# api/urls.py
from django.urls import path
from .views import MedicalRepresentativeInfo

urlpatterns = [
    path('med-rep-info/', MedicalRepresentativeInfo.as_view(), name='medical_representative_info'),
]