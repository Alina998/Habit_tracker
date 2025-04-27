from rest_framework import serializers
from habit_tracker.models import Habit


class RelatedAndAwardValidator:
    """Исключаем одновременный выбор связанной привычки related_habit и указания вознаграждения reward."""

    def __call__(self, value):
        related_habit = bool(dict(value).get("related_habit"))
        reward = bool(dict(value).get("reward"))

        if related_habit and reward:
            raise serializers.ValidationError(
                "Заполните только одно из полей: вознаграждение или связанная привычка."
            )


class HabitTimeToCompleteValidator:
    """Время выполнения должно быть не больше 120 секунд."""

    def __call__(self, value):
        time_to_complete = dict(value).get("time_to_complete")

        if isinstance(time_to_complete, int) and time_to_complete > 120:
            raise serializers.ValidationError(
                "Время выполнения привычки не должно превышать 120 секунд."
            )


class HabitRelatedHabitIsPleasantValidator:
    """В связанные привычки могут попадать только привычки с признаком приятной привычки."""

    def __call__(self, value):
        related_habit = dict(value).get("related_habit")
        if related_habit:
            habit = Habit.objects.get(pk=related_habit.pk)
            if not habit.is_pleasant_habit:
                raise serializers.ValidationError(
                    "Связанная привычка должна быть приятной"
                )


class HabitPleasantValidator:
    """Проверяем условие, что у приятной привычки не может быть вознаграждения или связанной привычки."""

    def __call__(self, value):
        is_pleasant_habit = dict(value).get("is_pleasant_habit")
        reward = bool(dict(value).get("reward"))
        related_habit = bool(dict(value).get("related_habit"))

        if is_pleasant_habit and reward or is_pleasant_habit and related_habit:
            raise serializers.ValidationError(
                "Приятная привычка не может иметь вознаграждение или связанную привычку."
            )


class HabitFrequencyValidator:
    """Нельзя выполнять привычку реже, чем 1 раз в 7 дней."""

    def __call__(self, value):
        frequency = dict(value).get("frequency")
        if isinstance(frequency, int) and frequency > 7:
            raise serializers.ValidationError(
                "Частота выполнения привычки должна быть от 1 до 7 дней."
            )
