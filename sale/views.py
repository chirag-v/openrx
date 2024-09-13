# sales/views.py
from django.shortcuts import render, redirect
from django.forms import modelformset_factory
from .models import Sale, SaleItem
from .forms import SaleForm, SaleItemForm
from django.contrib import messages
from django.core.paginator import Paginator


def create_sale(request):
    SaleItemFormSet = modelformset_factory(SaleItem, form=SaleItemForm, extra=0)
    if request.method == 'POST':
        form = SaleForm(request.POST)
        formset = SaleItemFormSet(request.POST, queryset=SaleItem.objects.none())

        if form.is_valid() and formset.is_valid():
            sale = form.save()
            for form in formset:
                sale_item = form.save(commit=False)
                sale_item.sale = sale
                sale_item.save()
            sale.calculate_total_amount()
            sale.calculate_net_amount()
            return redirect('sale_list')
    else:
        form = SaleForm()
        formset = SaleItemFormSet(queryset=SaleItem.objects.none())

    return render(request, 'sale/sale_invoice.html', {'form': form, 'formset': formset})


create_sale.view_name = 'Sales Invoice (Billing)'
create_sale.synonyms = ['Add Sale', 'Create Sale', 'Add New Sale', 'Create New Sale',
                        'Add Sale Invoice', 'Create Sale Invoice', 'Add New Sale Invoice',
                        'Create New Sale Invoice', 'Generate Sales Invoice', 'Generate Sale Invoice'
                        'make bill', 'make invoice', 'generate bill', 'generate invoice', 'create bill',
                        'create invoice']



def sale_list(request):
    search_query = request.GET.get('search', '')
    if search_query:
        sales = Sale.objects.filter(invoice_number__icontains=search_query).order_by('-id')
    else:
        sales = Sale.objects.all().order_by('-id')  # order by id to show the latest sale first

    paginator = Paginator(sales, 10)  # Show 10 sales per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'sale/sale_list.html', {'page_obj': page_obj})
sale_list.view_name = 'View Sales Bill(s)'
sale_list.synonyms = ['List Sales Bills', 'View Sales Invoices', 'List Sales Invoices', 'View Sales Bills']

