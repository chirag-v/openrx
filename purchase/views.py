# purchase/views.py
from django.db.models import Q, CharField
from django.db.models.functions import Cast
from django.shortcuts import render, redirect
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

        # Debugging: Print errors if form or formset is not valid
        print("Form fields:", form.fields.keys())

        if not form.is_valid():
            print("Purchase Form Errors:", form.errors)
        if not formset.is_valid():
            print("PurchaseItem Formset Errors:", formset.errors)
            for form in formset:
                print(form.errors)

        if form.is_valid() and formset.is_valid():
            purchase = form.save()
            for form in formset:
                purchase_item = form.save(commit=False)
                purchase_item.purchase = purchase
                purchase_item.calculate_amount()
                purchase_item.save()
            purchase.calculate_gross_amount()
            purchase.calculate_net_amount()
            messages.success(request,
                             'Purchase created successfully with Material Receipt (MR) Number : MR' + str(purchase.id))
            return redirect('purchase_list')
    else:
        form = PurchaseForm()
        formset = PurchaseItemFormSet(queryset=PurchaseItem.objects.none())

    return render(request, 'purchase/purchase_entry.html', {'form': form, 'formset': formset})


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

