from django.urls import path
from .views import create_item, item_list, edit_item, delete_item, get_item_gst, get_items


urlpatterns = [
    path('create', create_item, name='create_item'),
    path('list', item_list, name='item_list'),
    path('edit/<int:pk>/', edit_item, name='edit_item'),
    path('delete/<int:pk>/', delete_item, name='delete_item'),
    path('get_item_gst/<int:item_id>/', get_item_gst, name='get_item_gst'),
    path('get_items/', get_items, name='get_items'),

]
