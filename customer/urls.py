# customer/urls.py
from django.urls import path
from .views import customer_list, add_customer, edit_customer, delete_customer

urlpatterns = [
    path('customer_list', customer_list, name='customer_list'),
    path('add_customer', add_customer, name='add_customer'),
    path('edit_customer/<int:id>', edit_customer, name='edit_customer'),
    path('delete_customer/<int:id>', delete_customer, name='delete_customer'),
]
