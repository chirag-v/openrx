# gst/views.py
from django.http import JsonResponse
from .utils import get_state_name_by_code


# Create your views here.
def get_state_name(request):
    code = request.GET.get('code')
    state_name = get_state_name_by_code(code)
    return JsonResponse({'stateName': state_name})


get_state_name.view_name = 'Get State Name (API)'
get_state_name.synonyms = ['Get State Name', 'Fetch State Name', 'Get State Name by Code', 'Fetch State Name by Code',
                           'Get State Name API', 'Fetch State Name API', 'Get State Name by Code API',
                           'Fetch State Name by GST State Code API']