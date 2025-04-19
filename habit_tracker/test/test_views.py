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
        self.url = reverse("habit-list")

    def test_create_habit(self):
        data = {
            "action": "Пить воду",
            "place": "Дом",
            "time": "10:00:00",
            "frequency": 7,
            "time_to_complete": "00:05:00",
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_habits(self):
        Habit.objects.create(
            action="Пить воду",
            place="Дом",
            time="10:00:00",
            frequency=7,
            time_to_complete="00:05:00",
            user=self.user,
        )
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
