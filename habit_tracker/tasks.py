from celery import shared_task
import requests
from habit_tracker.models import Habit
from config.settings import TELEGRAM_TOKEN
from datetime import datetime, timedelta
from users.models import User


def send_message(text, chat_id):
    requests.post(
        url=f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
        data={"chat_id": chat_id, "text": text},
    )


@shared_task
def send_tg_message():
    """Отправка сообщения в Telegram"""
    time_now = datetime.now()
    start_time = time_now - timedelta(minutes=10)
    finish_time = time_now + timedelta(minutes=10)
    habits = Habit.objects.filter(time__gte=start_time, time__lte=finish_time)

    for habit in habits:
        action = habit.action
        place = habit.place
        time = habit.time
        time_to_complete = habit.time_to_complete
        user = habit.user

        # Получаем chat_id из профиля пользователя
        chat_id = user.telegram_chat_id

        text = (
            f"Я буду {action} "
            f"в {time} "
            f"в {place} "
            f"в течение {time_to_complete}"
        )

        # Отправляем сообщение только если chat_id существует
        if chat_id:
            send_message(text, chat_id)

        # Обновляем время привычки
        habit.time += timedelta(days=habit.frequency)
        habit.save()


def get_updates():
    """Получаем CHAT_ID"""
    response = requests.get(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getUpdates")
    return response.json()


def parser_updates(updates):
    for update in updates:
        if "message" in update and "chat" in update["message"]:
            chat_username = update["message"]["chat"].get("username")
            if chat_username:
                try:
                    user = User.objects.get(telegram_profile=chat_username)
                    user.telegram_chat_id = update["message"]["chat"]["id"]
                    user.save()
                except User.DoesNotExist:
                    continue
