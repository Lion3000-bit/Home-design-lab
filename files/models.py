from django.db import models


class StoredFile(models.Model):
    """Файл, загруженный пользователем в личное файловое хранилище."""

    user = models.ForeignKey(
        "accounts.CustomUser",
        on_delete=models.CASCADE,
        related_name="stored_files",
        verbose_name="Пользователь",
    )
    file = models.FileField(upload_to="uploads/", verbose_name="Файл")
    name = models.CharField(max_length=255, verbose_name="Название")
    size = models.BigIntegerField(default=0, verbose_name="Размер (байт)")
    content_type = models.CharField(max_length=100, blank=True, default="", verbose_name="Тип")
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="Загрузка")

    class Meta:
        verbose_name = "Файл"
        verbose_name_plural = "Файлы"
        ordering = ["-uploaded_at"]

    def __str__(self):
        return f"{self.name} ({self.user})"

    @property
    def size_human(self):
        size = self.size or self.file.size
        for unit in ("B", "KB", "MB", "GB"):
            if abs(size) < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} TB"

    def delete(self, *args, **kwargs):
        # Удаляем файл с диска при удалении записи
        if self.file:
            self.file.delete(save=False)
        return super().delete(*args, **kwargs)
