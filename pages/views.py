from django.shortcuts import render

from .models import SiteSettings


def home(request):
    return render(request, "pages/home.html", {"site_settings": SiteSettings.load()})
