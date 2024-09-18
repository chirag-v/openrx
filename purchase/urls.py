# purchase/urls.py
from django.urls import path
from .views import purchase_list, purchase_form, get_purchase_item_data

urlpatterns = [
    path('create', purchase_form, name='create_purchase'),

    path('purchase_list', purchase_list, name='purchase_list'),

    path('edit/<int:id>', purchase_form, name='edit_purchase'),
    
    path('get_purchase_item_data/<int:item_id>/', get_purchase_item_data, name='get_purchase_item_data'),
]