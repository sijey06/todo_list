from django.db import models

from core.generate_key import generate_primary_key


class Category(models.Model):
    """Модель Категории."""

    id = models.CharField(
        primary_key=True,
        max_length=16,
        default=generate_primary_key,
        editable=False,
        verbose_name="ID",
    )
    title = models.CharField(
        "Название",
        max_length=100,
        help_text="Название категории",
    )

    class Meta:
        ordering = ('title',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


class Task(models.Model):
    """Модель задачи."""

    id = models.CharField(
        primary_key=True,
        max_length=16,
        default=generate_primary_key,
        editable=False,
        verbose_name="ID",
    )
    telegram_user_id = models.BigIntegerField(
        verbose_name="Telegram User ID",
        help_text="Идентификатор пользователя в Telegram",
    )
    category = models.ManyToManyField(
        Category,
        verbose_name="Категории",
        help_text="Связанные категории задачи",
    )
    title = models.CharField(
        "Название",
        max_length=100,
        help_text="Краткое название задачи",
    )
    description = models.TextField(
        "Описание",
        help_text="Подробное описание задачи",
    )
    created_at = models.DateTimeField(
        "Дата создания",
        auto_now_add=True,
        help_text="Дата и время создания задачи",
    )
    due_date = models.DateTimeField(
        "Срок выполнения",
        help_text="Дата и время завершения задачи",
    )

    class Meta:
        ordering = ('created_at',)
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'

    def __str__(self):
        return f'{self.telegram_user_id}: {self.title}'
