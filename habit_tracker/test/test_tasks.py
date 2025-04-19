from django.test import TestCase
from habit_tracker.tasks import check_habits, send_telegram_notification
from habit_tracker.models import Habit
from unittest.mock import patch
from users.models import User


class HabitTasksTest(TestCase):
    @patch("habit_tracker.tasks.send_telegram_notification")
    def test_check_habits(self, mock_send_telegram_notification):
        # Создание пользователя и привычки
        user = User.objects.create_user(
            username="testuser", email="testuser@mail.ru", password="testpass"
        )
        habit = Habit.objects.create(
            action="Пить воду",
            place="Дом",
            time="10:00:00",
            frequency=7,
            user=user,
            time_to_complete="00:05:00",
        )

        # Запуск задачи
        check_habits()

        # Проверка, что уведомление было отправлено
        mock_send_telegram_notification.assert_called_once()

    @patch("requests.post")
    def test_send_telegram_notification(self, mock_post):
        chat_id = "123456"
        message = "Test message"
        send_telegram_notification(chat_id, message)

        # Проверка, что запрос был отправлен
        mock_post.assert_called_once()
