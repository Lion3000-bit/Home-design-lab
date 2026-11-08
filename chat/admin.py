from django.contrib import admin

from .models import ChatMessage


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ("user", "short_text", "created_at")
    list_filter = ("created_at",)
    search_fields = ("text", "user__email", "user__username")
    raw_id_fields = ("user",)

    @admin.display(description="Текст")
    def short_text(self, obj):
        return obj.text[:60]
