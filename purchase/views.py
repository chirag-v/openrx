# purchase/views.py
from django.db.models import Q, CharField
from django.db.models.functions import Cast
from django.shortcuts import render, redirect, get_object_or_404
from django.forms import modelformset_factory
from .models import Purchase, PurchaseItem
from .forms import PurchaseForm, PurchaseItemForm
from django.contrib import messages
from django.core.paginator import Paginator


def create_purchase(request):
    PurchaseItemFormSet = modelformset_factory(PurchaseItem, form=PurchaseItemForm, extra=0)
    if request.method == 'POST':
        form = PurchaseForm(request.POST)
        formset = PurchaseItemFormSet(request.POST, queryset=PurchaseItem.objects.none())

        if form.is_valid() and formset.is_valid():
            purchase = form.save()
            for form in formset:
                purchase_item = form.save(commit=False)
                purchase_item.purchase = purchase
                purchase_item.calculate_amount()
                purchase_item.save()
            purchase.calculate_gross_amount()
            purchase.calculate_net_amount()
            messages.success(request, 'Purchase created successfully with Material Receipt (MR) Number : MR' + str(purchase.id))
            return redirect('purchase_list')
        else:
            messages.error(request, 'There was an error with your submission. Please check the form and try again.')
    else:
        form = PurchaseForm()
        formset = PurchaseItemFormSet(queryset=PurchaseItem.objects.none())

    return render(request, 'purchase/purchase_entry.html', {'form': form, 'formset': formset})


create_purchase.view_name = 'Purchase Entry'
create_purchase.synonyms = ['Add Purchase', 'Create Purchase', 'Add New Purchase', 'Create New Purchase',
                            'Add Purchase Entry', 'Create Purchase Entry', 'Add New Purchase Entry',
                            'Create New Purchase Entry']


def purchase_list(request):
    search_query = request.GET.get('search', '')
    if search_query:
        purchases = Purchase.objects.annotate(
            id_str=Cast('id',CharField())
        ).filter(
            Q(invoice_number__icontains=search_query) |
            Q(id_str__icontains=search_query) |
            Q(supplier_name__name__icontains=search_query)

        ).order_by('-id')
    else:
        purchases = Purchase.objects.all().order_by('-id')  # order by id to show the latest purchase first

    paginator = Paginator(purchases, 10)  # Show 10 purchases per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'purchase/purchase_list.html', {'page_obj': page_obj})

purchase_list.view_name = 'List of Purchases'
purchase_list.synonyms = ['List Purchases', 'View Purchases', 'Show Purchases', 'Display Purchases', 'MR number list',
                          'Material Receipt number list', 'View List of Purchases']

def edit_purchase(request, pk):
    purchase = get_object_or_404(Purchase, pk=pk)
    PurchaseItemFormSet = modelformset_factory(PurchaseItem, form=PurchaseItemForm, extra=0, can_delete=True)

    if request.method == 'POST':
        form = PurchaseForm(request.POST, instance=purchase)
        formset = PurchaseItemFormSet(request.POST, queryset=PurchaseItem.objects.filter(purchase=purchase))

        if form.is_valid() and formset.is_valid():
            form.save()
            for form in formset:
                purchase_item = form.save(commit=False)
                purchase_item.purchase = purchase
                purchase_item.calculate_amount()
                purchase_item.save()
            purchase.calculate_gross_amount()
            purchase.calculate_net_amount()
            messages.success(request, 'Purchase updated successfully')
            return redirect('purchase_list')
        else:
            messages.error(request, 'There was an error with your submission. Please check the form and try again.')
    else:
        form = PurchaseForm(instance=purchase)
        formset = PurchaseItemFormSet(queryset=PurchaseItem.objects.filter(purchase=purchase))

    return render(request, 'purchase/purchase_entry.html', {'form': form, 'formset': formset})
