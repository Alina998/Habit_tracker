from django.db import models
from django.conf import settings


class Habit(models.Model):
    """Модель привычки"""

    name = models.CharField(max_length=100, verbose_name="Название привычки")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        blank=True,
        null=True,
    )
    place = models.CharField(max_length=100, verbose_name="Место")
    time = models.TimeField(verbose_name="Время")
    action = models.CharField(max_length=300, verbose_name="Описание привычки")
    is_pleasant_habit = models.BooleanField(
        default=False, verbose_name="Признак приятной привычки"
    )
    related_habit = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name="Связанная привычка",
    )
    frequency = models.PositiveIntegerField(default=1, verbose_name="Периодичность")
    reward = models.CharField(
        max_length=300, verbose_name="Вознаграждение за выполнение"
    )
    time_to_complete = models.DurationField(verbose_name="Время на выполнение привычки")
    is_public = models.BooleanField(default=False, verbose_name="Публичная привычка")

    def __str__(self):
        return f"Я буду {self.action} в {self.time} в {self.place}"

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
        # ordering = ("name",)
