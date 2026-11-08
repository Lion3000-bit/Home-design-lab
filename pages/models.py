from django.db import models


class SiteSettings(models.Model):
    """Персональные настройки сайта (одна запись-одиночка)."""

    SINGLETON_KEY = "main"

    key = models.CharField(max_length=50, unique=True, default=SINGLETON_KEY)
    site_name = models.CharField(max_length=100, default="Мой дом")
    tagline = models.CharField(max_length=200, blank=True, default="Домашний сайт")
    welcome_text = models.TextField(blank=True, default="")
    announcement = models.TextField(blank=True, default="")
    announcement_active = models.BooleanField(default=False)
    allow_registration = models.BooleanField(default=True)
    maintenance_mode = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Настройки сайта"
        verbose_name_plural = "Настройки сайта"

    objects = models.Manager()

    @classmethod
    def load(cls):
        obj, _created = cls.objects.get_or_create(
            key=cls.SINGLETON_KEY,
            defaults={
                "site_name": "Мой дом",
                "tagline": "Домашний сайт",
                "welcome_text": "",
                "announcement": "",
                "announcement_active": False,
                "allow_registration": True,
                "maintenance_mode": False,
            },
        )
        return obj

    def __str__(self):
        return f"Настройки: {self.site_name}"
