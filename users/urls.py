from django.urls import path
from rest_framework.permissions import AllowAny
from users.views import (
    UserRegistrationView,
    UserListAPIView,
    UserRetrieveAPIView,
    UserUpdateAPIView,
    UserDestroyAPIView,
    UserHabitListView,
    PublicHabitListView,
    HabitDetailView,
    UpdateTelegramChatIDView,
    TokenObtainPairView
)

app_name = "users"

urlpatterns = [
    path("users", UserListAPIView.as_view(), name="user_list"),
    path("register/", UserRegistrationView.as_view(), name="register"),
    path("login/", TokenObtainPairView.as_view(permission_classes=(AllowAny,)),name="login",),
    path("users/<int:pk>/", UserRetrieveAPIView.as_view(), name="user-detail"),
    path("users/<int:pk>/update/", UserUpdateAPIView.as_view(), name="user-update"),
    path("users/<int:pk>/delete/", UserDestroyAPIView.as_view(), name="user-delete"),
    path("users/habits/", UserHabitListView.as_view(), name="user_habits"),
    path("public-habits/", PublicHabitListView.as_view(), name="public_habits"),
    path("users/habits/<int:pk>/", HabitDetailView.as_view(), name="habit_detail"),
    path('update-telegram-chat-id/', UpdateTelegramChatIDView.as_view(), name='update-telegram-chat-id'),
]
