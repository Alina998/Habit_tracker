from habit_tracker.models import Habit
from habit_tracker.serializers import HabitSerializer
from habit_tracker.paginators import CustomPageNumberPagination
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny


class HabitCreateAPIView(generics.CreateAPIView):
    """Представление для создания привычки"""

    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class HabitListAPIView(generics.ListAPIView):
    """Представление для списка привычек"""

    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)


class HabitRetrieveAPIView(generics.RetrieveAPIView):
    """Представление для просмотра привычки"""

    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = [AllowAny]


class HabitUpdateAPIView(generics.UpdateAPIView):
    """Представление для обновления привычки"""

    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = [IsAuthenticated]


class HabitDestroyAPIView(generics.DestroyAPIView):
    """Представление для удаления привычки"""

    queryset = Habit.objects.all()
    permission_classes = [IsAuthenticated]


class PublicHabitListAPIView(generics.ListAPIView):
    """Представление для просмотра публичных привычек"""

    serializer_class = HabitSerializer
    queryset = Habit.objects.filter(is_public=True)
    permission_classes = [AllowAny]
    pagination_class = CustomPageNumberPagination
