from django.shortcuts import render, redirect, get_object_or_404
from .forms import ItemForm
from .models import Item
from django.http import JsonResponse
from django.db.models import Q



def create_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('item_list')
    else:
        form = ItemForm()

    return render(request, 'item/create_item.html', {'form': form})


def item_list(request):
    query = request.GET.get('search')
    if query:
        items = Item.objects.filter(
            Q(name__icontains=query) |
            Q(sku__icontains=query)
        )
    else:
        items = Item.objects.all()

    context = {
        'items': items,
        'search_query': query,
    }
    return render(request, 'item/item_list.html', context)


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


def get_item_gst(request, item_id):
    item = Item.objects.get(id=item_id)
    return JsonResponse({'gst': item.gst.percentage})


def get_items(request):
    items = Item.objects.all().values('id', 'name')
    return JsonResponse({'items': list(items)})