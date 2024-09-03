from django.urls import path
from .views import create_purchase

urlpatterns = [
    path('create', create_purchase, name='create_purchase'),
]