# company/views.py
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Company, Division, MedicalRepresentative
from .forms import CompanyForm, DivisionForm, MedicalRepresentativeForm  # Assuming you have a form for Company model
from django.core.paginator import Paginator
from django.db.models import Prefetch
from .mr_transfer import transfer_medical_representative, logger
import logging


def get_divisions(request, company_id):
    divisions = Division.objects.filter(company_id=company_id)
    data = {
        'divisions': [{'id': division.id, 'name': division.name} for division in divisions]
    }
    return JsonResponse(data)


def company_list(request):
    search_query = request.GET.get('search', '')
    if search_query:
        companies = Company.objects.filter(name__icontains=search_query)
    else:
        companies = Company.objects.all().order_by('-id') # Latest companies first

    paginator = Paginator(companies, 10)  # Show 10 companies per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'company/company_list.html', {'page_obj': page_obj})


company_list.view_name = 'List of Companies'
company_list.synonyms = ['List Companies', 'View Companies', 'Show Companies', 'Display Companies', 'View List of Companies', 'Show List of Companies', 'Display List of Companies']

# Company Create
# company/views.py

def add_or_edit_company(request, id=None):
    if id:
        company = get_object_or_404(Company, pk=id)
    else:
        company = None

    if request.method == 'POST':
        form = CompanyForm(request.POST, instance=company)
        if form.is_valid():
            form.save()
            return redirect('company_list')
    else:
        form = CompanyForm(instance=company)

    return render(request, 'company/add_company.html', {'form': form, 'is_edit': id is not None})

add_or_edit_company.view_name = 'Add or Edit Company'
add_or_edit_company.synonyms = ['Add Company', 'Edit Company', 'Create Company', 'Update Company']


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
    return render(request, 'company/add_company.html', {'form': form, 'company': company})


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


logger = logging.getLogger(__name__)

def add_or_edit_medical_representative(request, pk=None):
    if pk:
        representative = get_object_or_404(MedicalRepresentative, pk=pk)
        is_edit = True
    else:
        representative = MedicalRepresentative()
        is_edit = False

    if request.method == 'POST':
        form = MedicalRepresentativeForm(request.POST, instance=representative)
        if form.is_valid():
            representative = form.save(commit=False)
            if form.cleaned_data['division']:
                representative.company = form.cleaned_data['division'].company
            else:
                representative.company = form.cleaned_data['company']
            representative.save()
            return redirect('list_medical_representatives')  # Redirect to the list view
        else:
            logger.error(f"Form errors: {form.errors}")
    else:
        form = MedicalRepresentativeForm(instance=representative)

    return render(request, 'company/add_medical_representative.html', {
        'form': form,
        'is_edit': is_edit
    })


add_or_edit_medical_representative.view_name = 'Add Medical Representative'
add_or_edit_medical_representative.synonyms = ['Add MR', 'Create MR', 'Add New MR', 'Create New MR', 'Add Medical Representative', 'Create Medical Representative', 'Add New Medical Representative', 'Create New Medical Representative']

def edit_medical_representative(request, pk):
    representative = get_object_or_404(MedicalRepresentative, pk=pk)
    if request.method == 'POST':
        form = MedicalRepresentativeForm(request.POST, instance=representative)
        if form.is_valid():
            form.save()
            return redirect('list_medical_representatives')  # Redirect to a new URL
    else:
        form = MedicalRepresentativeForm(instance=representative)
    return render(request, 'company/add_medical_representative.html', {'form': form, 'representative': representative})


def list_medical_representatives(request):
    representatives = MedicalRepresentative.objects.all()
    return render(request, 'company/list_medical_representatives.html', {'representatives': representatives})

list_medical_representatives.view_name = 'List of Medical Representatives'
list_medical_representatives.synonyms = ['List MRs', 'View MRs', 'Show MRs', 'Display MRs', 'View List of MRs',
                                         'Show List of MRs', 'Display List of MRs']

def delete_medical_representative(request, pk):
    representative = get_object_or_404(MedicalRepresentative, pk=pk)
    if request.method == 'POST':
        representative.delete()
        return redirect('list_medical_representatives')
    return render(request, 'company/delete_medical_representative.html', {'representative': representative})



def get_med_rep_info(request):
    med_rep_id = request.GET.get('med_rep_id')
    med_rep = MedicalRepresentative.objects.get(id=med_rep_id)

    if med_rep.division:
        company_name = med_rep.division.company.name
        division_name = med_rep.division.name
        division_id = med_rep.division.id
    else:
        company_name = med_rep.company.name if med_rep.company else 'N/A'
        division_name = 'This company has no division'
        division_id = ''

    data = {
        'company': company_name,
        'division': division_name,
        'division_id': division_id
    }
    return JsonResponse(data)

get_med_rep_info.view_name = 'Get Medical Representative Info (API)'
get_med_rep_info.synonyms = ['Fetch MR Info', 'Retrieve MR Info', 'Get MR Info', 'Get Medical Representative Information',
                             'Fetch Medical Representative Info', 'Retrieve Medical Representative Info']


# company/views.py
def mr_transfer(request):
    medical_representatives = MedicalRepresentative.objects.all()
    companies = Company.objects.all()
    divisions = Division.objects.all()
    error_message = None

    if request.method == 'POST':
        med_rep_id = request.POST.get('med_rep_id')
        leaving_division_id = request.POST.get('leaving_division_id', None)
        joining_division_id = request.POST.get('joining_division_id', None)
        joining_company_id = request.POST.get('joining_company_id', None)

        logger.debug(f"med_rep_id: {med_rep_id}, leaving_division_id: {leaving_division_id}, joining_division_id: {joining_division_id}, joining_company_id: {joining_company_id}")

        success = transfer_medical_representative(med_rep_id, leaving_division_id, joining_division_id, joining_company_id)
        if success:
            return redirect('list_medical_representatives')  # Adjust the redirect as needed
        else:
            error_message = "An error occurred during the transfer. Please try again."

    return render(request, 'company/mr_transfer.html', {
        'medical_representatives': medical_representatives,
        'companies': companies,
        'divisions': divisions,
        'error_message': error_message
    })

mr_transfer.view_name = 'Transfer MR'
mr_transfer.synonyms = ['Move MR', 'Relocate MR', 'Transfer MR', 'Transfer Medical Representative']
