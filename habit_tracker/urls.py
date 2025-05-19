from django.urls import path
from habit_tracker.views import (
    HabitCreateAPIView,
    HabitListAPIView,
    HabitRetrieveAPIView,
    HabitUpdateAPIView,
    HabitDestroyAPIView,
    PublicHabitListAPIView,
)

app_name = "habit_tracker"

urlpatterns = [
    path("create/", HabitCreateAPIView.as_view(), name="habit_create"),
    path("", HabitListAPIView.as_view(), name="user_habits"),
    path("<int:pk>/", HabitRetrieveAPIView.as_view(), name="habit"),
    path("update/<int:pk>/", HabitUpdateAPIView.as_view(), name="habit_update"),
    path("delete/<int:pk>/", HabitDestroyAPIView.as_view(), name="habit_delete"),
    path("public/", PublicHabitListAPIView.as_view(), name="habit_public"),
]
