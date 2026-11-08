from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, UpdateView, View

from accounts.models import CustomUser
from files.models import StoredFile
from pages.models import SiteSettings
from .forms import SiteSettingsForm


class DashboardHomeView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = "dashboard/home.html"

    def test_func(self):
        return self.request.user.is_staff

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        s = SiteSettings.load()
        context["site_settings"] = s
        context["total_users"] = CustomUser.objects.count()
        context["active_users"] = CustomUser.objects.filter(is_active=True).count()
        context["staff_users"] = CustomUser.objects.filter(is_staff=True).count()
        context["total_files"] = StoredFile.objects.count()
        context["storage_used"] = (
            StoredFile.objects.aggregate(total_size=Sum("size"))["total_size"] or 0
        )
        context["recent_users"] = CustomUser.objects.order_by("-date_joined")[:5]
        context["recent_files"] = StoredFile.objects.select_related("user").order_by("-uploaded_at")[:5]
        return context


class DashboardSettingsView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = SiteSettings
    form_class = SiteSettingsForm
    template_name = "dashboard/settings.html"
    success_url = reverse_lazy("dashboard:home")

    def test_func(self):
        return self.request.user.is_staff

    def get_object(self, queryset=None):
        # Используем уже готовый в вашей модели метод load()
        return SiteSettings.load()



class DashboardUsersView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_staff

    def get(self, request, *args, **kwargs):
        users = CustomUser.objects.all().order_by("email")
        return render(request, "dashboard/users.html", {"users": users})


class DashboardUserActionView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_staff

    def post(self, request, *args, **kwargs):
        user = get_object_or_404(CustomUser, pk=kwargs.get("pk"))
        action = kwargs.get("action")
        if action == "role":
            user.is_staff = not user.is_staff
            user.save(update_fields=["is_staff"])
        elif action == "toggle_active":
            user.is_active = not user.is_active
            user.save(update_fields=["is_active"])
        elif action == "delete" and user != request.user:
            user.delete()
        return redirect("dashboard:users")
