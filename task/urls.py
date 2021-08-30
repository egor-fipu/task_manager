from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import TaskViewSet, TaskHistoryViewSet

router = SimpleRouter()

router.register('tasks', TaskViewSet, basename='task')
router.register('task-history', TaskHistoryViewSet, basename='task_history')

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('', include(router.urls)),
]
