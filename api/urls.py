# api/urls.py
from django.urls import path
from rest_framework.schemas import get_schema_view
from rest_framework.renderers import JSONOpenAPIRenderer

from .views import MedicalRepresentativeInfo, GetStateName, GetItems

app_name = 'api'

# Define the schema view directly in the URLs
schema_view = get_schema_view(
    title="API Schema",
    description="All available API endpoints in the project.",
    version="1.0.0",
    renderer_classes=[JSONOpenAPIRenderer]
)

urlpatterns = [
    path('med-rep-info/', MedicalRepresentativeInfo.as_view(), name='medical_representative_info'),
    path('get-state-name/', GetStateName.as_view(), name='get_state_name'),
    path('get-items/', GetItems.as_view(), name='get_items'),
    path('endpoints/', schema_view, name='api_endpoints'),  # Use drf-spectacular for schema generation
]