from django.core.exceptions import ValidationError


class HabitValidator:
    """Валидатор привычек"""

    def __call__(self, habit):
        # Исключаем одновременный выбор связанной привычки related_habit и указания вознаграждения reward.
        if habit.reward and habit.related_habit:
            raise ValidationError(
                "Заполните только одно из полей: вознаграждение или связанная привычка."
            )

        # Время выполнения должно быть не больше 120 секунд.
        if habit.time_to_complete.total_seconds() > 120:
            raise ValidationError(
                "Время выполнения привычки не должно превышать 120 секунд."
            )

        # В связанные привычки могут попадать только привычки с признаком приятной привычки.
        if habit.related_habit and not habit.related_habit.is_pleasant_habit:
            raise ValidationError("Связанная привычка должна быть приятной.")

        # Проверяем условие, что у приятной привычки не может быть вознаграждения или связанной привычки.
        if habit.is_pleasant_habit:
            if habit.reward or habit.related_habit:
                raise ValidationError(
                    "Приятная привычка не может иметь вознаграждение или связанную привычку."
                )

        # Нельзя выполнять привычку реже, чем 1 раз в 7 дней.
        if habit.frequency < 1 or habit.frequency > 7:
            raise ValidationError(
                "Частота выполнения привычки должна быть от 1 до 7 дней."
            )
