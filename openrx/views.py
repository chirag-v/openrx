# openrx/views.py

import re
from django.apps import apps
from django.urls import resolve, reverse, NoReverseMatch
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .forms import LoginForm
from django.http import JsonResponse

from rest_framework.views import APIView
from rest_framework.schemas import get_schema_view
from rest_framework.renderers import CoreJSONRenderer, JSONRenderer

def get_apps_and_features() -> object:
    apps_and_features = []
    for app_config in apps.get_app_configs():
        if app_config.name.startswith('django.') or str(app_config.path).startswith(str(settings.BASE_DIR)) is False:
            continue

        app_name = app_config.verbose_name
        features = []

        try:
            app_urls = __import__(f'{app_config.name}.urls', fromlist=['urlpatterns'])
            for pattern in getattr(app_urls, 'urlpatterns', []):
                try:
                    view_func = resolve(reverse(pattern.name)).func
                    view_class = getattr(view_func, 'view_class', None)
                    if view_class:
                        view_name = getattr(view_class, 'view_name', view_class.__name__)
                    else:
                        view_name = getattr(view_func, 'view_name', view_func.__name__) if pattern.name else 'Unnamed View'
                        # Check if the view_func has a view_name attribute
                        if hasattr(view_func, 'view_name'):
                            view_name = view_func.view_name
                    features.append({'name': view_name, 'url': reverse(pattern.name)})
                except NoReverseMatch:
                    continue
        except ImportError:
            continue

        # Sort features alphabetically by name
        features.sort(key=lambda feature: feature['name'])
        apps_and_features.append({'name': app_name, 'features': features})

    # Sort apps alphabetically by name
    apps_and_features.sort(key=lambda app: app['name'])

    return apps_and_features

def handle_dynamic_url(pattern):
    """
    Handle dynamic URLs by inserting dummy values for URL parameters.
    """
    # Get the regex pattern for the URL and replace dynamic segments with dummy values
    try:
        url_pattern = pattern.pattern.regex.pattern

        # Substitute dynamic parts like '<int:id>' or '<str:slug>' with dummy values
        url_pattern = re.sub(r'<int:\w+>', '1', url_pattern)
        url_pattern = re.sub(r'<str:\w+>', 'dummy', url_pattern)
        url_pattern = re.sub(r'<slug:\w+>', 'dummy-slug', url_pattern)
        url_pattern = re.sub(r'<uuid:\w+>', '123e4567-e89b-12d3-a456-426614174000', url_pattern)

        # Attempt to resolve the cleaned URL pattern
        return url_pattern
    except Exception as e:
        return None


def homepage(request):
    apps_and_features = get_apps_and_features()
    return render(request, 'homepage.html', {'apps_and_features': apps_and_features})



def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('homepage')  # Redirect to a home page or dashboard
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

login_view.view_name = 'Secure Login'
login_view.synonyms = ['Signin', 'Log in']  # Synonyms for the view name


def logout_view(request):
    logout(request)
    return redirect('login')

logout_view.view_name = 'Logout'
logout_view.synonyms = ['Signout', 'Log out', 'Log off']  # Synonyms for the view name


# openrx/views.py

def search_view(request):
    query = request.GET.get('q', '')
    results = []
    if query:
        apps_and_features = get_apps_and_features()
        for app in apps_and_features:
            for feature in app['features']:
                feature_name = feature['name'].lower()
                synonyms = getattr(resolve(feature['url']).func, 'synonyms', [])
                if query.lower() in feature_name or any(query.lower() in synonym.lower() for synonym in synonyms):
                    results.append({'name': feature['name'], 'url': feature['url']})
    return JsonResponse({'results': results})



