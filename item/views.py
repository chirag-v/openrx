# item/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ItemForm
from .models import Item
from django.http import JsonResponse
from django.db.models import Q
from django.core.paginator import Paginator


def create_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('item_list')
    else:
        form = ItemForm()
    return render(request, 'item/create_item.html', {'form': form})

create_item.view_name = 'Add New Item'
create_item.synonyms = ['Add Product', 'Create Product', 'Add New Product', 'Create New Product',
                        'Add Item', 'Create Item', 'Create New Item']


def item_list(request):
    query = request.GET.get('search')
    if query:
        items = Item.objects.filter(
            Q(name__icontains=query) |
            Q(sku__icontains=query)
        )
    else:
        items = Item.objects.all().order_by('-id')  # order by id to show the latest item first
    paginator = Paginator(items, 10)  # Show 10 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'search_query': query,
    }
    return render(request, 'item/item_list.html', context)

item_list.view_name = 'List of Items'
item_list.synonyms = ['List Products', 'View Products', 'Show Products', 'Display Products', 'View List of Products',
                      'Show List of Products', 'Display List of Products', 'View Items', 'Show Items',
                      'Display Items', 'View List of Items', 'Show List of Items', 'Display List of Items']


def edit_item(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect('item_list')
    else:
        form = ItemForm(instance=item)
    return render(request, 'item/edit_item.html', {'form': form, 'item': item})


def delete_item(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('item_list')
    return render(request, 'item/delete_item.html', {'item': item})


# item/views.py
def get_item_gst(request, item_id):
    try:
        item = Item.objects.get(id=item_id)
        gst_rate = item.gst.rate
        return JsonResponse({
            'gst': {
                'percentage': gst_rate.percentage,
                'description': gst_rate.description
            }
        })
    except Item.DoesNotExist:
        return JsonResponse({'error': 'Item not found'}, status=404)