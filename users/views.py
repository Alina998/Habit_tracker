from rest_framework import generics, permissions, status, views
from users.models import User
from users.serializers import UserSerializer, MyTokenObtainPairSerializer
from habit_tracker.models import Habit
from rest_framework_simplejwt.views import TokenObtainPairView
from habit_tracker.serializers import HabitSerializer
from habit_tracker.paginators import CustomPageNumberPagination
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class UserRegistrationView(generics.CreateAPIView):
    """Представление для регистрации пользователя"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]  # Доступно для всех


class UserListAPIView(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserRetrieveAPIView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)


class UserUpdateAPIView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(user=self.request.user)

class UserDestroyAPIView(generics.DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(user=self.request.user)


class UserHabitListView(generics.ListCreateAPIView):
    """Представление для просмотра привычек пользователя"""

    serializer_class = HabitSerializer
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)

    @api_view(["POST"])
    @permission_classes([IsAuthenticated])
    def perform_create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PublicHabitListView(generics.ListAPIView):
    """Представление для просмотра публичных привычек"""

    serializer_class = UserSerializer
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        return Habit.objects.filter(is_public=True)

    @api_view(["POST"])
    @permission_classes([IsAuthenticated])
    def perform_create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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


class MyTokenObtainPairView(TokenObtainPairView):
    """Представление для получения токена"""

    serializer_class = MyTokenObtainPairSerializer


class UpdateTelegramChatIDView(views.APIView):
    def post(self, request):
        telegram_chat_id = request.data.get('telegram_chat_id')
        user = request.user  # Предполагается, что пользователь аутентифицирован

        if not telegram_chat_id:
            return Response({"error": "Отсутствует telegram_chat_id."}, status=status.HTTP_400_BAD_REQUEST)

        user.telegram_chat_id = telegram_chat_id
        user.save()

        return Response({"message": "Telegram_chat_id успешно обновлен."}, status=status.HTTP_200_OK)
