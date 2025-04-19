from rest_framework import viewsets
from habit_tracker.models import Habit
from habit_tracker.serializers import HabitSerializer
from habit_tracker.validators import HabitValidator


class HabitViewSet(viewsets.ModelViewSet):
    """Представление для привычки"""

    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    validator = HabitValidator()

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user
        )  # Устанавливаем текущего пользователя как создателя привычки
