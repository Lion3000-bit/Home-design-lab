from django.contrib.auth import login as auth_login
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View

from pages.models import SiteSettings

from .forms import ChangePasswordForm, ProfileForm, RegisterForm
from .models import CustomUser


class RegisterView(View):
    template_name = "accounts/register.html"
    form_class = RegisterForm

    def dispatch(self, request, *args, **kwargs):
        if not SiteSettings.load().allow_registration:
            return redirect("pages:home")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["site_settings"] = SiteSettings.load()
        return context

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {"form": self.form_class()})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect("pages:home")
        return render(request, self.template_name, {"form": form, "site_settings": SiteSettings.load()})


class LoginView(auth_views.LoginView):
    template_name = "accounts/login.html"
    redirect_authenticated_user = True
    success_url = reverse_lazy("pages:home")


class LogoutView(auth_views.LogoutView):
    next_page = reverse_lazy("pages:home")


class ProfileView(LoginRequiredMixin, View):
    template_name = "accounts/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = ProfileForm(instance=self.request.user)
        context["change_password_form"] = ChangePasswordForm(user=self.request.user)
        return context

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data())

    def post(self, request, *args, **kwargs):
        form = ProfileForm(request.POST, instance=request.user)
        context = self.get_context_data()
        context["form"] = form
        if form.is_valid():
            form.save()
            return redirect("accounts:profile")
        return render(request, self.template_name, context)


class ChangePasswordView(View):
    template_name = "accounts/password_change.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(f"{settings.LOGIN_URL}/login/")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {"form": ChangePasswordForm(user=request.user)})

    def post(self, request, *args, **kwargs):
        form = ChangePasswordForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect("accounts:profile")
        return render(request, self.template_name, {"form": form, "site_settings": SiteSettings.load()})
