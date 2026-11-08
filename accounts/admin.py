from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from .models import CustomUser, UserLink


@admin.register(CustomUser)
class UserAdmin(DjangoUserAdmin):
    model = CustomUser
    list_display = ("email", "username", "full_name", "is_staff", "is_active", "date_joined")
    list_filter = ("is_staff", "is_active", "is_superuser")
    search_fields = ("email", "username", "first_name", "last_name")
    ordering = ("email",)
    fieldsets = (
        (None, {"fields": ("password",)}),
        (
            "Личные данные",
            {"fields": ("email", "username", "first_name", "last_name", "bio", "avatar")},
        ),
        (
            "Права",
            {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")},
        ),
        ("Метаданные", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            "Создание пользователя",
            {
                "classes": ("wide",),
                "fields": ("email", "username", "password1", "password2", "is_staff", "is_superuser"),
            },
        ),
    )


@admin.register(UserLink)
class UserLinkAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "url", "created_at")
    list_filter = ("created_at",)
    search_fields = ("title", "url", "user__email", "user__username")
    raw_id_fields = ("user",)

