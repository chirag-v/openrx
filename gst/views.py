from django.http import JsonResponse
from .utils import get_state_name_by_code


# Create your views here.
def get_state_name(request):
    code = request.GET.get('code')
    state_name = get_state_name_by_code(code)
    return JsonResponse({'stateName': state_name})

