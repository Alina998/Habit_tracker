from rest_framework import viewsets, status
from habit_tracker.models import Habit
from habit_tracker.serializers import HabitSerializer
from habit_tracker.validators import HabitValidator
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from habit_tracker.serializers import HabitSerializer
from habit_tracker.paginators import CustomPageNumberPagination


class HabitViewSet(viewsets.ModelViewSet):
    """Представление для привычки"""

    serializer_class = HabitSerializer
    pagination_class = CustomPageNumberPagination

    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    validator = HabitValidator()

    @api_view(['POST'])
    @permission_classes([IsAuthenticated])
    def perform_create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) # Устанавливаем текущего пользователя как создателя привычки
