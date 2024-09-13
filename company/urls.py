# company/urls.py
# customer/urls.py
from django.urls import path
from .views import (company_list, delete_company, division_list, division_edit,
                    division_create, division_delete, get_divisions, add_or_edit_company,
                    add_or_edit_medical_representative, list_medical_representatives, delete_medical_representative)

urlpatterns = [
    path('company_list', company_list, name='company_list'),
    path('add_company', add_or_edit_company, name='add_company'),
    path('edit_company/<int:id>', add_or_edit_company, name='edit_company'),
    path('delete_company/<int:id>', delete_company, name='delete_company'),
    path('divisions', division_list, name='division_list'),
    path('divisions/create', division_create, name='division_create'),
    path('divisions/edit/<int:pk>', division_edit, name='division_edit'),
    path('divisions/delete/<int:pk>', division_delete, name='division_delete'),
    path('add_medical_representative', add_or_edit_medical_representative, name='add_medical_representative'),
    path('edit_medical_representative/<int:id>', add_or_edit_medical_representative, name='edit_medical_representative'),
    path('delete_medical_representative/<int:pk>', delete_medical_representative, name='delete_medical_representative'),
    path('list_medical_representatives', list_medical_representatives, name='list_medical_representatives'),
    path('get-divisions/<int:company_id>/', get_divisions, name='get_divisions'),
]
