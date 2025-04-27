from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from users.models import User
from habit_tracker.models import Habit


class UserTestCase(APITestCase):
    """Тестирование модели пользователя"""

    def setUp(self):
        self.user = User.objects.create_user(
            email="testuser@example.com",
            password="testpassword",
            username="test_user",
            telegram_profile="TGnik",
            telegram_chat_id="12340",
        )
        self.habit = Habit.objects.create(
            action="Пить воду",
            place="Дом",
            time="10:00:00",
            frequency=7,
            user=self.user,
            time_to_complete="00:05:00",
        )

    def test_create_user(self):
        """Тест для создания пользователя"""
        url = reverse("users:register")
        data = {
            "email": "newuser@example.com",
            "password": "newpassword",
            "username": "newuser",
            "telegram_profile": "TGnik1",
            "telegram_chat_id": "1234500",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)  # Один существующий + один новый

    def test_get_user(self):
        """Тест для просмотра данных пользователя"""
        self.client.force_authenticate(self.user)
        url = reverse("users:user-detail", args=[self.user.id])
        response = self.client.get(url)
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get("email"), self.user.email)
