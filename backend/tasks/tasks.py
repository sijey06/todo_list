from celery import shared_task
from django.core.cache import cache
from django.utils import timezone

from backend.celery import app

from .models import Task


@app.task(name="send_reminder")
def send_reminder(task_id):
    """Создание ключа для Redis."""
    task = Task.objects.get(pk=task_id)
    cache.set(f"reminder_{task.id}", task.telegram_user_id)
    task.notification_sent = True
    task.save()


@shared_task(name="check_due_dates")
def check_due_dates():
    """Проверка задач на условия."""
    now = timezone.now()
    tasks = Task.objects.filter(due_date__lte=now, notification_sent=False)
    for task in tasks:
        send_reminder.delay(task.id)
        task.notification_sent = True
        task.save()
