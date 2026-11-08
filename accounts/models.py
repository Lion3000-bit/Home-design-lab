from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError("Email обязателен")
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, username, password, **extra_fields)


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[UnicodeUsernameValidator()],
        help_text="Имя пользователя",
    )
    first_name = models.CharField(max_length=150, blank=True, default="")
    last_name = models.CharField(max_length=150, blank=True, default="")
    bio = models.TextField(blank=True, default="")
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip() or self.username

    @property
    def initials(self):
        parts = (self.first_name, self.last_name)
        initials = "".join(p[0] for p in parts if p).upper()
        if not initials:
            initials = (self.username or "?")[:1].upper()
        return initials

    @property
    def is_admin(self):
        return self.is_staff or self.is_superuser


class UserLink(models.Model):
    """Ссылка, которую пользователь добавил на свою страницу ссылок."""

    user = models.ForeignKey(
        "accounts.CustomUser",
        on_delete=models.CASCADE,
        related_name="user_links",
        verbose_name="Пользователь",
    )
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    url = models.URLField(verbose_name="Ссылка")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создана")

    class Meta:
        verbose_name = "Ссылка пользователя"
        verbose_name_plural = "Ссылки пользователей"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} ({self.user})"
