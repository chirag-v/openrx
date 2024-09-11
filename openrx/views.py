# openrx/views.py
from django.apps import apps
from django.shortcuts import render
from django.urls import resolve, reverse
from django.conf import settings


def get_apps_and_features():
    apps_and_features = []
    for app_config in apps.get_app_configs():
        # Convert settings.BASE_DIR to a string with str()
        if app_config.name.startswith('django.') or str(app_config.path).startswith(str(settings.BASE_DIR)) is False:
            continue

        app_name = app_config.verbose_name
        features = []

        try:
            app_urls = __import__(f'{app_config.name}.urls', fromlist=['urlpatterns'])
            for pattern in getattr(app_urls, 'urlpatterns', []):
                try:
                    view_name = resolve(reverse(pattern.name)).func.__name__ if pattern.name else 'Unnamed View'
                    features.append({'name': view_name, 'url': reverse(pattern.name)})
                except:
                    continue
        except ImportError:
            continue

        apps_and_features.append({'name': app_name, 'features': features})

    return apps_and_features

def homepage(request):
    apps_and_features = get_apps_and_features()
    return render(request, 'homepage.html', {'apps_and_features': apps_and_features})

