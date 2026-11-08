from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.http import FileResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import ListView

from pages.models import SiteSettings

from .models import StoredFile


class FileListView(LoginRequiredMixin, ListView):
    model = StoredFile
    template_name = "files/list.html"
    context_object_name = "files"

    def get_queryset(self):
        return StoredFile.objects.filter(user=self.request.user).order_by("-uploaded_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["site_settings"] = SiteSettings.load()
        usage = (
            StoredFile.objects.filter(user=self.request.user)
            .aggregate(total_size=Sum("size"))["total_size"]
            or 0
        )
        context["storage_used"] = usage
        context["storage_limit"] = 50 * 1024 * 1024
        context["storage_percent"] = min(100, int(usage * 100 / (50 * 1024 * 1024)))
        return context

    def post(self, request, *args, **kwargs):
        uploaded = request.FILES.getlist("files")
        if not uploaded:
            return redirect("files:list")
        for f in uploaded:
            StoredFile.objects.create(
                user=request.user,
                file=f,
                name=f.name,
                size=f.size,
                content_type=f.content_type or "application/octet-stream",
            )
        return redirect("files:list")

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class PublicFilesView(LoginRequiredMixin, ListView):
    """Просмотр файлов всех пользователей (доступно любому авторизованному)."""

    model = StoredFile
    template_name = "files/public_list.html"
    context_object_name = "files"

    def get_queryset(self):
        return (
            StoredFile.objects.select_related("user")
            .all()
            .order_by("-uploaded_at")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["site_settings"] = SiteSettings.load()
        return context


class FileDeleteView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        obj = get_object_or_404(StoredFile, id=kwargs.get("pk"), user=request.user)
        obj.delete()
        return redirect("files:list")


class FileDownloadView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        obj = get_object_or_404(StoredFile, id=kwargs.get("pk"), user=request.user)
        response = FileResponse(obj.file.open("rb"), as_attachment=True, filename=obj.name)
        return response
