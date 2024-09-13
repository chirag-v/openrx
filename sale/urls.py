# sales/urls.py
from django.urls import path
from .views import create_sale, sale_list

urlpatterns = [
    path('create', create_sale, name='create_sale'),  # URL for creating a new sale
    path('sale_list', sale_list, name='sale_list'),  # URL for listing all sales
]
