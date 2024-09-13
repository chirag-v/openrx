# supplier/views.py
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from .models import Supplier
from .forms import SupplierForm
from django.http import JsonResponse

def get_gstin(request, supplier_id):
    supplier = Supplier.objects.get(id=supplier_id)
    return JsonResponse({'gstin': supplier.gstin})

def supplier_list(request):
    search_query = request.GET.get('search', '')
    if search_query:
        suppliers = Supplier.objects.filter(
            Q(name__icontains=search_query) |
            Q(gstin__icontains=search_query) |
            Q(mobile__icontains=search_query)
        ).order_by('name')  # Added line to order by name
    else:
        suppliers = Supplier.objects.all().order_by('name')

    paginator = Paginator(suppliers, 10)  # 10 suppliers per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'supplier/supplier_list.html', {'page_obj': page_obj, 'search_query': search_query})


supplier_list.view_name = 'List of Suppliers'
supplier_list.synonyms = ['List Suppliers', 'View Suppliers', 'Show Suppliers', 'Display Suppliers',
                            'Show List of Suppliers', 'Display List of Suppliers', 'View Vendors', 'Show Vendors',
                            'Display Vendors', 'View List of Vendors', 'Show List of Vendors', 'Display List of Vendors',
                            'View Sellers', 'Show Sellers', 'Display Sellers', 'View List of Sellers',
                            'Display List of Sellers', 'View Stockists', 'Show Stockists', 'Display Stockists',
                            'View List of Stockists', 'Show List of Stockists', 'Display List of Stockists',
                            'View Distributors', 'Show Distributors', 'Display Distributors', 'Show Wholesalers',
                            'Show List of Distributors', 'Display List of Distributors', 'View Wholesalers',
                            'Display Wholesalers', 'View List of Wholesalers', 'Show List of Wholesalers']

def add_supplier(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('supplier_list')
    else:
        form = SupplierForm()
    return render(request, 'supplier/add_supplier.html', {'form': form})


add_supplier.view_name = 'Add New Supplier'
add_supplier.synonyms = ['Add Supplier', 'Create Supplier', 'Add New Supplier', 'Create New Supplier', 'Add Vendor',
                         'Create Vendor', 'Add New Vendor', 'Create New Vendor', 'Add Seller', 'Create Seller', 'Stockist',
                         'Distributor', 'Wholesaler', 'Add Distributor', 'Create Distributor', 'Add New Distributor',
                         'Create New Distributor', 'Add Wholesaler', 'Create Wholesaler', 'Add New Wholesaler',
                         'Create New Wholesaler', 'Add Stockist', 'Create Stockist', 'Add New Stockist', 'Create New Stockist',
                         'Add Seller', 'Create Seller', 'Add New Seller', 'Create New Seller']


def edit_supplier(request, id):
    supplier = Supplier.objects.get(pk=id)
    if request.method == 'POST':
        form = SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            form.save()
            return redirect('supplier_list')
    else:
        form = SupplierForm(instance=supplier)
    return render(request, 'supplier/edit_supplier.html', {'form': form})


def delete_supplier(request, id):
    supplier = get_object_or_404(Supplier, pk=id)
    if request.method == 'POST':  # Confirm deletion
        supplier.delete()
        return redirect('supplier_list')
    return render(request, 'supplier/delete_supplier.html', {'supplier': supplier})

