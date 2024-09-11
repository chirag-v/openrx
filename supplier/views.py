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


def add_supplier(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('supplier_list')
    else:
        form = SupplierForm()
    return render(request, 'supplier/add_supplier.html', {'form': form})


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

