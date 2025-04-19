from rest_framework import generics, permissions
from users.models import User
from users.serializers import UserSerializer
from habit_tracker.models import Habit


class UserRegistrationView(generics.CreateAPIView):
    """Представление для регистрации пользователя"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]  # Доступно для всех


class UserLoginView(generics.GenericAPIView):
    """Представление для аутентификации пользователя"""

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")


class UserHabitListView(generics.ListCreateAPIView):
    """Представление для просмотра привычек пользователя"""

    serializer_class = UserSerializer

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)


class PublicHabitListView(generics.ListAPIView):
    """Представление для просмотра публичных привычек"""

    serializer_class = UserSerializer

    def get_queryset(self):
        return Habit.objects.filter(is_public=True)


class HabitDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Представление для просмотра деталей привычки"""

    serializer_class = UserSerializer

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Представление для просмотра пользователя"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # Позволяет пользователям видеть и редактировать только свои данные
        return self.request.user
