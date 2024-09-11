# purchase/views.py
from django.shortcuts import render, redirect
from django.forms import modelformset_factory
from .models import Purchase, PurchaseItem
from .forms import PurchaseForm, PurchaseItemForm
from django.contrib import messages

# views.py

def purchase_entry(request):
    form = PurchaseForm()
    return render(request, 'purchase/purchase_entry.html', {'form': form})


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
    purchases = Purchase.objects.all().order_by('-id')  # order by id to show the latest purchase first
    return render(request, 'purchase/purchase_list.html', {'purchases': purchases})