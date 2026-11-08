from django.db import models


class Folder(models.Model):
    """Папка в личном хранилище пользователя (иерархия, как в Google Drive)."""

    user = models.ForeignKey(
        "accounts.CustomUser",
        on_delete=models.CASCADE,
        related_name="folders",
        verbose_name="Пользователь",
    )
    name = models.CharField(max_length=255, verbose_name="Название")
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children",
        verbose_name="Родительская папка",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создана")

    class Meta:
        verbose_name = "Папка"
        verbose_name_plural = "Папки"
        ordering = ["name"]
        unique_together = ("user", "parent", "name")

    def __str__(self):
        return self.name

    def get_breadcrumbs(self):
        """Возвращает список папок от корня к текущей для хлебных крошек."""
        crumbs = []
        current = self
        while current:
            crumbs.append(current)
            current = current.parent
        return list(reversed(crumbs))

    def get_path(self):
        return " / ".join(f.name for f in self.get_breadcrumbs())


class StoredFile(models.Model):
    """Файл в личном хранилище пользователя."""

    user = models.ForeignKey(
        "accounts.CustomUser",
        on_delete=models.CASCADE,
        related_name="stored_files",
        verbose_name="Пользователь",
    )
    folder = models.ForeignKey(
        Folder,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="files",
        verbose_name="Папка",
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
        for unit in ("Б", "КБ", "МБ", "ГБ"):
            if abs(size) < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} ТБ"

    def delete(self, *args, **kwargs):
        if self.file:
            self.file.delete(save=False)
        return super().delete(*args, **kwargs)
