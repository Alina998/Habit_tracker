from rest_framework import generics
from users.models import User
from users.serializers import UserSerializer, MyTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated, AllowAny
from users.permissions import IsModerator, IsOwner


class UserRegistrationView(generics.CreateAPIView):
    """Представление для регистрации пользователя"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]  # Доступно для всех


class UserListAPIView(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsModerator]


class UserRetrieveAPIView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)


class UserUpdateAPIView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)


class UserDestroyAPIView(generics.DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Представление для просмотра пользователя"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_object(self):
        # Позволяет пользователям видеть и редактировать только свои данные
        return self.request.user


class MyTokenObtainPairView(TokenObtainPairView):
    """Представление для получения токена"""

    serializer_class = MyTokenObtainPairSerializer
