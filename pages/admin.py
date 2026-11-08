from django.contrib import admin

from .models import SiteSettings


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ("key", "site_name", "tagline", "allow_registration", "maintenance_mode", "updated_at")
    list_editable = ("allow_registration", "maintenance_mode")
    search_fields = ("site_name", "tagline", "welcome_text")
    fields = (
        "key",
        "site_name",
        "tagline",
        "welcome_text",
        "announcement",
        "announcement_active",
        "allow_registration",
        "maintenance_mode",
        "updated_at",
    )
