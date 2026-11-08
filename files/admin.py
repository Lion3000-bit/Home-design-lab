from django.contrib import admin

from .models import StoredFile


@admin.register(StoredFile)
class StoredFileAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "name", "size", "content_type", "uploaded_at")
    list_filter = ("user", "content_type")
    search_fields = ("name",)
    raw_id_fields = ("user",)
