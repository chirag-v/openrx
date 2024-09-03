from django.shortcuts import render, redirect
from django.forms import modelformset_factory
from .models import PurchaseItem
from .forms import PurchaseForm, PurchaseItemForm


def create_purchase(request):
    PurchaseItemFormSet = modelformset_factory(PurchaseItem, form=PurchaseItemForm, extra=1)
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
            return redirect('purchase_list')
    else:
        form = PurchaseForm()
        formset = PurchaseItemFormSet(queryset=PurchaseItem.objects.none())
    return render(request, 'purchase/purchase_entry.html', {'form': form, 'formset': formset})