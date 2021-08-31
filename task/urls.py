from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import TaskViewSet, TaskHistoryViewSet

router_v1 = SimpleRouter()

router_v1.register('tasks', TaskViewSet, basename='task')
router_v1.register('task-history', TaskHistoryViewSet, basename='task_history')

urlpatterns = [
    path('v1/auth/', include('djoser.urls')),
    path('v1/auth/', include('djoser.urls.authtoken')),
    path('v1/', include(router_v1.urls)),
]
