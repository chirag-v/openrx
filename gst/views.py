# gst/views.py
from django.shortcuts import render

from django.shortcuts import render

def gst_view(request):
    return render(request, 'gst/gst_coming_soon.html')

gst_view.view_name = 'GSTR-1 Utility (Coming Soon)'