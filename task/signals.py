from django.db.models.signals import post_save
from django.dispatch import Signal

from task.models import TaskHistory, Task

update_task = Signal(providing_args=['instance', 'validated_data'])


def update_task_dispatcher(sender, **kwargs):
    """Сохраняет изменения задачи для истории"""
    if kwargs['validated_data']:
        TaskHistory.objects.create(
            **kwargs['validated_data'],
            task_id=kwargs['instance'].id
        )


update_task.connect(update_task_dispatcher)


def post_save_dispatcher(sender, **kwargs):
    """Сохраняет вновь созданную задачу для истории"""
    if kwargs['created']:
        TaskHistory.objects.create(
            task=kwargs['instance'],
            title=kwargs['instance'].title,
            description=kwargs['instance'].description,
            status=kwargs['instance'].status,
            plan_complet_date=kwargs['instance'].plan_complet_date,
        )


post_save.connect(post_save_dispatcher, sender=Task)
