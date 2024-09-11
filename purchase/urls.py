# purchase/urls.py
from django.urls import path
from .views import create_purchase, purchase_list

urlpatterns = [
    path('create', create_purchase, name='create_purchase'),

    path('purchase_list', purchase_list, name='purchase_list'),
]