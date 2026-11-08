from django.shortcuts import render

from .models import SiteSettings


def home(request):
    return render(request, "pages/home.html", {"site_settings": SiteSettings.load()})


def error_404(request, exception):
    return render(request, "errors/404.html", {"site_settings": SiteSettings.load()}, status=404)


def error_403(request, exception=None):
    return render(request, "errors/403.html", {"site_settings": SiteSettings.load()}, status=403)


def error_500(request):
    return render(request, "errors/500.html", {"site_settings": SiteSettings.load()}, status=500)
