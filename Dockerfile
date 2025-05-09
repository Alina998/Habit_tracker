FROM python:3.12-slim

# Устанавливаем рабочую директорию в контейнере
WORKDIR /habit_tracker

# Устанавливаем зависимости системы
RUN apt-get update
RUN apt-get install -y gcc libpq-dev
RUN apt-get clean
RUN rm -rf /var/lib/apt/lists/*


# Копируем файл зависимостей в контейнер
COPY requirements.txt ./

# Устанавливаем зависимости Python
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код приложения в контейнер
COPY . .

# Определяем переменные окружения
ENV SECRET_KEY=SECRET_KEY
ENV CELERY_BROKER_URL="redis://redis:6379/0"
ENV CELERY_BACKEND="redis://redis:6379/0"

# Создаем директорию для медиафайлов
RUN mkdir -p /habit_tracker/media

# Пробрасываем порт, который будет использовать Django
EXPOSE 8000

# Команда для запуска приложения
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]