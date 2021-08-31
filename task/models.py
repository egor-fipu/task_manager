from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

STATUS = (
    ('new', 'новая'),
    ('planned', 'запланированная'),
    ('in_progress', 'в работе'),
    ('completed', 'завершенная'),
)


class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=200)
    created = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True
    )
    status = models.CharField(max_length=11, choices=STATUS)
    finished = models.DateField(
        'Планируемая дата окончания',
        blank=True,
        null=True
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='tasks'
    )

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f'id:{self.id}, {self.title}'


class TaskHistory(models.Model):
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name='history'
    )
    title = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(max_length=200, blank=True, null=True)
    status = models.CharField(
        max_length=11, choices=STATUS,
        blank=True,
        null=True
    )
    finished = models.DateField(blank=True, null=True)
    date_change = models.DateTimeField(
        'Дата изменения',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        ordering = ['-date_change']
