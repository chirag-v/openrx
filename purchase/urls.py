# purchase/urls.py
from django.urls import path
from .views import purchase_list, purchase_form

urlpatterns = [
    path('create', purchase_form, name='create_purchase'),

    path('purchase_list', purchase_list, name='purchase_list'),

    path('edit/<int:id>', purchase_form, name='edit_purchase'),
]