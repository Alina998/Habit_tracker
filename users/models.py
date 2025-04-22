from django.contrib.auth.models import AbstractUser
from django.db import models
from users.managers import CustomUserManager


class User(AbstractUser):
    """Модель пользователя"""

    username = models.CharField(
        max_length=100,
        unique=True,
        blank=True,
        null=True,
        verbose_name="Имя пользователя",
    )
    email = models.EmailField(unique=True, verbose_name="Почта")
    phone_number = models.CharField(
        max_length=35, blank=True, null=True, verbose_name="Номер телефона"
    )
    user_country = models.CharField(
        max_length=56, blank=True, null=True, verbose_name="Страна"
    )
    user_photo = models.ImageField(
        upload_to="users/avatars",
        blank=True,
        null=True,
        verbose_name="Фото",
        help_text="Загрузите фото",
    )
    telegram_chat_id = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="Уникальный идентификатор чата"
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
