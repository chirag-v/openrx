# customer/views.py
from django.core.paginator import Paginator
from django.db.models import Q, CharField, Case, When
from django.shortcuts import render, redirect, get_object_or_404
from .models import Customer
from .forms import CustomerForm


def customer_list(request):
    search_query = request.GET.get('search', '')
    if search_query:
        customers = Customer.objects.annotate(
            ordering_field=Case(
                When(firm_name__isnull=False, then='firm_name'),
                default='name',
                output_field=CharField(),
            )
        ).filter(
            Q(name__icontains=search_query) |
            Q(mobile__icontains=search_query) |
            Q(firm_name__icontains=search_query) |
            Q(surname__icontains=search_query)  # Added line to include surname in search
        ).order_by('ordering_field')
    else:
        customers = Customer.objects.annotate(
            ordering_field=Case(
                When(firm_name__isnull=False, then='firm_name'),
                default='name',
                output_field=CharField(),
            )
        ).order_by('ordering_field')

    paginator = Paginator(customers, 10)  # Show 10 customers per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'customer/customer_list.html',  {'page_obj': page_obj, 'search_query': search_query})


customer_list.view_name = 'Customer List'
customer_list.synonyms = ['List Customers', 'View Customers', 'Show Customers', 'Display Customers', 'List of Customers', 'View List of Customers', 'Show List of Customers', 'Display List of Customers', 'Delete Customer', 'Edit Customer', 'Search Customer', 'Search Customers', 'Find Customer', 'Find Customers', 'Search for Customer', 'Search for Customers', 'Find for Customer', 'Find for Customers', 'Search Customer List', 'Search Customers List', 'Find Customer List', 'Find Customers List', 'Search for Customer List', 'Search for Customers List', 'Find for Customer List', 'Find for Customers List', 'Delete Customer List', 'Edit Customer List', 'Search Customer List', 'Search Customers List', 'Find Customer List', 'Find Customers List', 'Search for Customer List', 'Search for Customers List', 'Find for Customer List', 'Find for Customers List', 'Delete Customer List', 'Edit Customer List', 'Search Customer List', 'Search Customers List', 'Find Customer List', 'Find Customers List', 'Search for Customer List', 'Search for Customers List', 'Find for Customer List', 'Find for Customers List', 'Delete Customer List', 'Edit Customer List', 'Search Customer List', 'Search Customers List', 'Find Customer List', 'Find Customers List', 'Search for Customer List', 'Search for Customers List', 'Find for Customer List', 'Find for Customers List', 'Delete Customer List', 'Edit Customer List', 'Search Customer List', 'Search Customers List', 'Find Customer List', 'Find Customers List', 'Search for Customer List', 'Search for Customers List', 'Find for Customer List', 'Find for Customers List', 'Delete Customer List', 'Edit Customer List', 'Search Customer List', 'Search Customers List', 'Find Customer List', 'Find Customers List', 'Search for Customer List', 'Search for Customers List', 'Find for Customer List', 'Find for Customers List', 'Delete Customer List', 'Edit Customer List', 'Search Customer List', 'Search Customers List', 'Find Customer List', 'Find Customers List', 'Search for Customer List', 'Search for Customers List', 'Find for Customer List', 'Find for Customers List', 'Delete Customer List', 'Edit Customer List', 'Search Customer List', 'Search Customers List', 'Find Customer List', 'Find Customers List', 'Search for Customer List', 'Search for Customers List', 'Find for Customer List', 'Find for Customers List', 'Delete Customer List', 'Edit Customer List', 'Search Customer List', 'Search Customers List']


def add_customer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('customer_list')
    else:
        form = CustomerForm()
    return render(request, 'customer/add_customer.html', {'form': form})


add_customer.view_name = 'Add New Customer'
add_customer.synonyms = ['Add Customer', 'Create Customer', 'Add New Customer', 'Create New Customer']


def edit_customer(request, id):
    customer = Customer.objects.get(pk=id)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('customer_list')
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'customer/edit_customer.html', {'form': form, 'customer': customer})


def delete_customer(request, id):
    customer = get_object_or_404(Customer, pk=id)
    if request.method == 'POST':  # Confirm deletion
        customer.delete()
        return redirect('customer_list')
    return render(request, 'customer/delete_customer.html', {'customer': customer})



