from rest_framework import serializers

from task.models import Task, TaskHistory
from .signals import update_task


class TaskSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        fields = '__all__'
        model = Task

    def update(self, instance, validated_data):
        super(TaskSerializer, self).update(instance, validated_data)
        # при обновлении задачи вызываем сигнал для сохранения истории
        update_task.send(
            sender=self.__class__,
            instance=instance,
            validated_data=validated_data
        )
        return instance


class TaskHistorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'title',
            'description',
            'status',
            'plan_complet_date',
            'date_change'
        )
        model = TaskHistory


class HistoryTaskSerializer(serializers.ModelSerializer):
    history = TaskHistorySerializer(many=True, read_only=True)
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        fields = (
            'id',
            'title',
            'description',
            'created',
            'status',
            'plan_complet_date',
            'author',
            'history'
        )
        model = Task
