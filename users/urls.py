from django.urls import path
from users.views import (
    UserRegistrationView,
    UserLoginView,
    UserHabitListView,
    PublicHabitListView,
    HabitDetailView,
)

app_name = "users"

urlpatterns = [
    path("register/", UserRegistrationView.as_view(), name="register"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("habits/", UserHabitListView.as_view(), name="user_habits"),
    path("public-habits/", PublicHabitListView.as_view(), name="public_habits"),
    path("habits/<int:pk>/", HabitDetailView.as_view(), name="habit_detail"),
]
