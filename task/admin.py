from django.contrib import admin

from .models import Task, TaskHistory


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'description',
        'created',
        'status',
        'plan_complet_date',
        'author'
    )
    empty_value_display = '-пусто-'


admin.site.register(TaskHistory)
