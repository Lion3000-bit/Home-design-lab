from django.contrib import admin

from .models import Folder, StoredFile


@admin.register(Folder)
class FolderAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "parent", "created_at")
    list_filter = ("user", "created_at")
    search_fields = ("name", "user__email")
    raw_id_fields = ("user", "parent")


@admin.register(StoredFile)
class StoredFileAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "name", "folder", "size", "content_type", "uploaded_at")
    list_filter = ("user", "content_type", "folder")
    search_fields = ("name",)
    raw_id_fields = ("user", "folder")
