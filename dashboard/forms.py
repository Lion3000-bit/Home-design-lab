from django import forms
from django.forms import ModelForm

from pages.models import SiteSettings


class SiteSettingsForm(ModelForm):
    class Meta:
        model = SiteSettings
        fields = (
            "site_name",
            "tagline",
            "welcome_text",
            "announcement",
            "announcement_active",
            "allow_registration",
            "maintenance_mode",
        )
