from celery import shared_task
from django.utils import timezone
import requests
from habit_tracker.models import Habit
from config.settings import TELEGRAM_TOKEN


@shared_task
def check_habits():
    now = timezone.now()
    current_time = now.time()

    # Получаем все привычки для текущего дня
    habits_to_remind = Habit.objects.filter(time=current_time, user__is_active=True)

    for habit in habits_to_remind:
        chat_id = habit.user.profile.telegram_chat_id
        message = f"Время выполнять привычку: {habit.action} в {habit.place}!"

        send_telegram_notification.delay(chat_id, message)


@shared_task
def send_telegram_notification(chat_id, message):
    TOKEN = TELEGRAM_TOKEN
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": message, "parse_mode": "HTML"}
    response = requests.post(url, json=payload)
    return response.json()
