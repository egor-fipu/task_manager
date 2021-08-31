from rest_framework import serializers

from .models import Task, TaskHistory
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

    def validate_finished(self, value):
        if self.instance and value < self.instance.created.date():
            raise serializers.ValidationError(
                'Планируемая дата завершения '
                'не может быть ранее даты добавления'
            )
        return value


class TaskHistorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'title',
            'description',
            'status',
            'finished',
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
            'finished',
            'author',
            'history'
        )
        model = Task
