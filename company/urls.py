# customer/urls.py
from django.urls import path
from .views import (company_list, add_company, edit_company, delete_company, division_list, division_edit,
                    division_create, division_delete, add_medical_representative, edit_medical_representative,
                    get_divisions)

urlpatterns = [
    path('company_list', company_list, name='company_list'),
    path('add_company', add_company, name='add_company'),
    path('edit_company/<int:id>', edit_company, name='edit_company'),
    path('delete_company/<int:id>', delete_company, name='delete_company'),
    path('divisions', division_list, name='division_list'),
    path('divisions/create', division_create, name='division_create'),
    path('divisions/edit/<int:pk>', division_edit, name='division_edit'),
    path('divisions/delete/<int:pk>', division_delete, name='division_delete'),
    path('add_medical_representative', add_medical_representative, name='add_medical_representative'),
    path('edit_medical_representative/<int:pk>', edit_medical_representative, name='edit_medical_representative'),
    path('get-divisions/<int:company_id>/', get_divisions, name='get_divisions'),
]
