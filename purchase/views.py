# purchase/views.py
from django.db import transaction
from django.db.models import Q, CharField
from django.db.models.functions import Cast
from django.shortcuts import render, redirect, get_object_or_404
from django.forms import modelformset_factory
from .models import Purchase, PurchaseItem
from django.http import JsonResponse
from .forms import PurchaseForm, PurchaseItemForm
from django.core.paginator import Paginator



def purchase_list(request):
    search_query = request.GET.get('search', '')
    if search_query:
        purchases = Purchase.objects.annotate(
            id_str=Cast('id', CharField())
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


PurchaseItemFormSet = modelformset_factory(PurchaseItem, form=PurchaseItemForm, extra=1)

def purchase_form(request, id=None):
    if id:
        # Editing an existing purchase
        purchase = get_object_or_404(Purchase, id=id)
        form_title = "Edit Purchase"
        submit_button_text = "Update"
        queryset = PurchaseItem.objects.filter(purchase=purchase)
        is_editing = True  # Set flag to indicate editing mode
    else:
        # Creating a new purchase
        purchase = None
        form_title = "Create Purchase"
        submit_button_text = "Submit"
        queryset = PurchaseItem.objects.none()
        is_editing = False  # Set flag to indicate creation mode

    if request.method == "POST":
        form = PurchaseForm(request.POST, instance=purchase)
        formset = PurchaseItemFormSet(request.POST, queryset=queryset)

        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                purchase = form.save()
                purchase_items = formset.save(commit=False)
                for item in purchase_items:
                    item.purchase = purchase
                    item.save()
                formset.save_m2m()
            return redirect('purchase_list')  # Redirect to a purchase list or detail view
    else:
        form = PurchaseForm(instance=purchase)
        formset = PurchaseItemFormSet(queryset=queryset)

    # Pass the flag to the template
    return render(request, 'purchase/purchase_entry.html', {
        'form': form,
        'formset': formset,
        'form_title': form_title,
        'submit_button_text': submit_button_text,
        'is_editing': is_editing,  # Pass the editing flag
    })

purchase_form.view_name = 'Purchase Entry'
purchase_form.synonyms = ['Purchase Entry', 'Purchase Invoice', 'Purchase Create', 'Purchase Bill Entry']

def get_purchase_item_data(request, item_id):
    try:
        purchase_item = PurchaseItem.objects.get(item_id=item_id)

        return JsonResponse({
            'mrp': purchase_item.mrp,
            'purchase_rate': purchase_item.purchase_rate
        })
    except PurchaseItem.DoesNotExist:
        return JsonResponse({'error': 'Purchase item not found'}, status=404)