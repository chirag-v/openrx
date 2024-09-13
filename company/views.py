# company/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Company, Division, MedicalRepresentative
from .forms import CompanyForm, DivisionForm, MedicalRepresentativeForm  # Assuming you have a form for Company model
from django.core.paginator import Paginator
from django.db.models import Prefetch
from django.http import JsonResponse


def get_divisions(request, company_id):
    divisions = Division.objects.filter(company_id=company_id).values('id', 'name', 'company__name')
    formatted_divisions = [
        {"id": division["id"], "name": f"({division['company__name']}) - {division['name']}"}
        for division in divisions
    ]
    return JsonResponse(formatted_divisions, safe=False)


def company_list(request):
    search_query = request.GET.get('search', '')
    if search_query:
        companies = Company.objects.filter(name__icontains=search_query)
    else:
        companies = Company.objects.all()

    paginator = Paginator(companies, 10)  # Show 10 companies per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'company/company_list.html', {'page_obj': page_obj})


company_list.view_name = 'List of Companies'
company_list.synonyms = ['List Companies', 'View Companies', 'Show Companies', 'Display Companies', 'View List of Companies', 'Show List of Companies', 'Display List of Companies']

# Company Create
def add_company(request):
    if request.method == 'POST':
        form = CompanyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('company_list')
    else:
        form = CompanyForm()
    return render(request, 'company/add_company.html', {'form': form})
add_company.view_name = 'Add New Company'
add_company.synonyms = ['Add Company', 'Create Company', 'Add New Company', 'Create New Company']


# Company Edit
def edit_company(request, id):
    company = get_object_or_404(Company, pk=id)
    if request.method == 'POST':
        form = CompanyForm(request.POST, instance=company)
        if form.is_valid():
            form.save()
            return redirect('company_list')  # Redirect to the list of companies or appropriate page
    else:
        form = CompanyForm(instance=company)
    return render(request, 'company/edit_company.html', {'form': form, 'company': company})


# Company Delete
def delete_company(request, id):
    company = get_object_or_404(Company, pk=id)
    if request.method == 'POST':  # Confirm deletion
        company.delete()
        return redirect('company_list')
    return render(request, 'company/delete_company.html', {'company': company})


# Division Views
# Division List

def division_list(request):
    search_query = request.GET.get('search', '')
    companies_with_all_divisions = Company.objects.none()
    divisions_matching_search = Division.objects.none()

    if search_query:
        # Companies matching the search query
        companies_with_all_divisions = Company.objects.filter(
            name__icontains=search_query
        ).prefetch_related(
            Prefetch(
                'divisions',
                queryset=Division.objects.order_by('name'),
                to_attr='ordered_divisions'
            )
        ).distinct()

        # Divisions matching the search query and their companies
        divisions_matching_search = Division.objects.filter(
            name__icontains=search_query
        ).select_related('company').order_by('name')

        # Prepare a list of companies from divisions matching the search
        companies_from_divisions = {division.company for division in divisions_matching_search}

        # Combine companies from both queries, avoiding duplicates
        combined_companies = set(companies_with_all_divisions) | companies_from_divisions

        # Prepare final companies list with appropriate divisions
        final_companies = []
        for company in combined_companies:
            if company in companies_with_all_divisions:
                # Add company with all divisions
                final_companies.append(company)
            else:
                # Add company with only matching divisions
                matching_divisions = [division for division in divisions_matching_search if division.company_id == company.id]
                company.ordered_divisions = matching_divisions
                final_companies.append(company)
    else:
        # If no search query, get all companies and their divisions
        final_companies = Company.objects.order_by('name').prefetch_related(
            Prefetch(
                'divisions',
                queryset=Division.objects.order_by('name'),
                to_attr='ordered_divisions'
            )
        )

    # Apply pagination
    paginator = Paginator(list(final_companies), 10)  # Adjust the number per page as needed
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'divisions/division_list.html', {'page_obj': page_obj, 'search_query': search_query})

division_list.view_name = 'List of Divisions'
division_list.synonyms = ['List Divisions', 'View Divisions', 'Show Divisions', 'Display Divisions',
                          'View List of Divisions', 'Show List of Divisions', 'Display List of Divisions']

# Division Create
def division_create(request):
    if request.method == 'POST':
        form = DivisionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('division_list')
    else:
        form = DivisionForm()
    return render(request, 'divisions/division_form.html', {'form': form})

division_create.view_name = 'Create Division (of Company)'
division_create.synonyms = ['Add Division', 'Create Division', 'Add New Division', 'Create New Division',
                            'Add Division to Company', 'Create Division for Company', 'Add New Division to Company',
                            'Create New Division for Company']


# Division Edit
def division_edit(request, pk):
    division = Division.objects.get(pk=pk)
    if request.method == 'POST':
        form = DivisionForm(request.POST, instance=division)
        if form.is_valid():
            form.save()
            return redirect('division_list')
    else:
        form = DivisionForm(instance=division)
    return render(request, 'divisions/division_form.html', {'form': form})

# Delete Division
def division_delete(request, pk):
    division = Division.objects.get(pk=pk)
    if request.method == 'POST':
        division.delete()
        return redirect('division_list')
    context = {'division': division, 'company': division.company}
    return render(request, 'divisions/division_delete.html', context)

# Medical Representative Views
def add_medical_representative(request):
    if request.method == 'POST':
        form = MedicalRepresentativeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('company_list')  # Redirect to a new URL
    else:
        form = MedicalRepresentativeForm()
    return render(request, 'company/add_medical_representative.html', {'form': form})

add_medical_representative.view_name = 'Add Medical Representative'
add_medical_representative.synonyms = ['Add MR', 'Create MR', 'Add New MR', 'Create New MR', 'Add Medical Representative', 'Create Medical Representative', 'Add New Medical Representative', 'Create New Medical Representative']

def edit_medical_representative(request, pk):
    representative = get_object_or_404(MedicalRepresentative, pk=pk)
    if request.method == 'POST':
        form = MedicalRepresentativeForm(request.POST, instance=representative)
        if form.is_valid():
            form.save()
            return redirect('add_company')  # Redirect to a new URL
    else:
        form = MedicalRepresentativeForm(instance=representative)
    return render(request, 'company/edit_medical_representative.html', {'form': form, 'representative': representative})