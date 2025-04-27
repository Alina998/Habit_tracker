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
    habits = Habit.objects.filter(time__gte=start_time).filter(time__lte=finish_time)

    for habit in habits:
        action = habit.action
        place = habit.place
        time = habit.time
        time_complete = habit.time_complete
        user_tg = habit.user.telegram

        updates = get_updates()
        if updates["ok"]:
            parser_updates(updates["result"])

        chat_id = User.objects.get(telegram=user_tg).chat_id

        text = (
            f"Привычка {action} "
            f"в {place} "
            f"должна выполняться {time} "
            f"на протяжении {time_complete}"
        )
        send_message(text, chat_id)

        habit.time += timedelta(days=habit.frequency)
        habit.save()


def get_updates():
    """Получаем CHAT_ID"""

    response = requests.get(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getUpdates")
    return response.json()


def parser_updates(updates):
    for update in updates:
        user = User.objects.get(telegram=update["message"]["chat"]["username"])
        if User.objects.filter(telegram=user).exist():
            user.chat_id = update["message"]["chat"]["id"]
            user.update_id = update["update_id"]
            user.save()
