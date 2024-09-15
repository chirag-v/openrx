# api/urls.py
from django.urls import path
from .views import MedicalRepresentativeInfo, GetStateName, GetItems

urlpatterns = [
    path('med-rep-info/', MedicalRepresentativeInfo.as_view(), name='medical_representative_info'),
    path('get-state-name/', GetStateName.as_view(), name='get_state_name'),
    path('get-items/', GetItems.as_view(), name='get_items')
]
