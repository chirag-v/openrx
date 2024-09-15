# customer/urls.py
from django.urls import path
from .views import customer_form, customer_list, delete_customer

urlpatterns = [
    path('customer_list', customer_list, name='customer_list'),
    path('add_customer', customer_form, name='add_customer'),
    path('edit_customer/<int:id>', customer_form, name='edit_customer'),
    path('delete_customer/<int:id>', delete_customer, name='delete_customer'),
]
