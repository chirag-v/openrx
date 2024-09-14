# openrx/urls.py
"""
URL configuration for openrx project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from openrx.views import homepage, login_view, logout_view, search_view


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', homepage, name='homepage'),
    path('api/', include('api.urls')),
    path('customer/', include('customer.urls')),
    path('supplier/', include('supplier.urls')),
    path('company/', include('company.urls')),
    path('gst/', include('gst.urls')),
    path('item/', include('item.urls')),
    path('purchase/', include('purchase.urls')),
    path('sale/', include('sale.urls')),
    path('inventory/', include('inventory.urls')),
    path('secure-gateway/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('search/', search_view, name='search'),

]


# Remove or comment out this block in production
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
