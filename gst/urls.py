# gst/urls.py
from django.urls import path
from .views import get_state_name

urlpatterns = [



path('get-state-name', get_state_name, name='get_state_name'),
    ]