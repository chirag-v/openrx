# supplier/urls.py
from django.urls import path
from .views import supplier_list, add_supplier, edit_supplier, delete_supplier, get_gstin
urlpatterns = [
    path('supplier_list', supplier_list, name='supplier_list'),
    path('add_supplier', add_supplier, name='add_supplier'),
    path('edit_supplier/<int:id>', edit_supplier, name='edit_supplier'),
    path('delete_supplier/<int:id>', delete_supplier, name='delete_supplier'),
    path('get_gstin/<int:supplier_id>/', get_gstin, name='get_gstin'),

]