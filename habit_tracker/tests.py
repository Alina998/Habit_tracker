from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from habit_tracker.models import Habit
from users.models import User


class HabitViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="testuser@mail.ru", password="testpass"
        )
        self.client.login(email="testuser@mail.ru", password="testpass")
        self.url = reverse("users:user_habits")

        self.client.force_authenticate(user=self.user)

    def test_create_habit(self):
        """Тест для создания привычки"""
        data = {
            "action": "Пить воду",
            "place": "Дом",
            "time": "10:00:00",
            "frequency": 7,
            "time_to_complete": "00:05:00",
        }

        habit_create_url = reverse("habit_tracker:habit-create")
        response = self.client.post(habit_create_url, data=data)

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )
        print(response.json())

        self.assertEqual(response.json().get("name"), data.get("name"))

        self.assertTrue(Habit.objects.get(pk=self.habit.pk).name, data.get("name"))

    def test_list_habits(self):
        url = reverse("users:user_habits")
        Habit.objects.create(
            action="Пить воду",
            place="Дом",
            time="10:00:00",
            frequency=7,
            time_to_complete="00:05:00",
            user=self.user,
        )

        print(url)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)