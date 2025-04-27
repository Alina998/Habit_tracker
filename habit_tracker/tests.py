from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from habit_tracker.models import Habit
from users.models import User


class HabitTestCase(APITestCase):
    """Тест модели привычки"""

    def setUp(self):
        """Создаем пользователя для теста"""
        self.user = User.objects.create_user(
            username="testuser", email="testuser@mail.ru", password="testpass"
        )

        """Авторизация"""
        self.client.force_authenticate(user=self.user)

        """Создаем привычку"""
        self.habit = Habit.objects.create(
            name="Утренняя пробежка",
            user=self.user,
            action="Бегать",
            place="В парке",
            time="10:00:00",
            is_pleasant_habit=True,
            frequency=3,
            time_to_complete="00:05:00",
            reward="Контрастный душ",
            is_public=True,
        )

    def test_create_habit(self):
        """Тест для создания привычки"""
        data = {
            "name": "Водный баланс",
            "action": "Пить воду",
            "place": "Дом",
            "time": "10:00:00",
            "frequency": 7,
            "time_to_complete": "00:05:00",
            "reward": "Здоровая кожа",
            "is_public": True,
        }

        habit_create_url = reverse("habit_tracker:habit_create")
        response = self.client.post(habit_create_url, data=data)

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )
        print(response.json())

        new_habit_id = response.json().get("id")

        self.assertEqual(response.json().get("name"), data.get("name"))

        new_habit = Habit.objects.get(pk=new_habit_id)
        self.assertEqual(new_habit.name, data.get("name"))

    def test_list_habits(self):
        """Тест для просмотра списка привычек"""
        url = reverse("habit_tracker:user_habits")

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            Habit.objects.get(pk=self.habit.pk).name,
            response.json().get("results")[0].get("name"),
        )

    def test_update_habit(self):
        """Тест для обновления привычки"""

        data = {
            "place": "updated place",
            "action": "updated action",
            "reward": "updated reward",
        }

        habit_update_url = reverse("habit_tracker:habit_update", args=[self.habit.pk])

        response = self.client.patch(habit_update_url, data)

        print(response.json())

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        response = response.json()

        self.assertEqual(response.get("place"), "updated place")
        self.assertEqual(response.get("action"), "updated action")

    def test_delete_habit(self):
        """Тест для удаления привычки"""

        habit_delete_url = reverse("habit_tracker:habit_delete", args=[self.habit.pk])

        response = self.client.delete(habit_delete_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )
        self.assertFalse(Habit.objects.filter(pk=self.habit.pk).exists())

    def test_public_habits(self):
        """Тест для просмотра списка публичных привычек"""
        url = reverse("habit_tracker:habit_public")

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            Habit.objects.get(pk=self.habit.pk).name,
            response.json().get("results")[0].get("name"),
        )
