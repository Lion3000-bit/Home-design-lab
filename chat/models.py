from django.db import models

from accounts.models import CustomUser


class ChatMessage(models.Model):
    """Сообщение в общем чате всех пользователей."""

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="chat_messages",
        verbose_name="Пользователь",
    )
    text = models.TextField(verbose_name="Текст сообщения")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Отправлено")

    class Meta:
        verbose_name = "Сообщение чата"
        verbose_name_plural = "Сообщения чата"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.full_name}: {self.text[:30]}"
