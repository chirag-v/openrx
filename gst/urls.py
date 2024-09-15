# gst/urls.py
from django.urls import path
from .views import gst_view

urlpatterns = [
    path('', gst_view, name='gst_view'),
]