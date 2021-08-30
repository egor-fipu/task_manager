from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, mixins

from task.models import Task
from task.serializers import TaskSerializer, HistoryTaskSerializer


class TaskViewSet(viewsets.ModelViewSet):
    """Создание, просмотр, изменение задачи"""
    serializer_class = TaskSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('status', 'plan_complet_date')

    def get_queryset(self):
        new_queryset = Task.objects.filter(author=self.request.user)
        return new_queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class RetrieveViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    pass


class TaskHistoryViewSet(RetrieveViewSet):
    """Просмотр истории изменений задачи"""
    serializer_class = HistoryTaskSerializer

    def get_queryset(self):
        new_queryset = Task.objects.filter(author=self.request.user)
        return new_queryset
