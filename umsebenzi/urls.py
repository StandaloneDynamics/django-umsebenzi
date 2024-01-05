from rest_framework import routers

from umsebenzi.views import ProjectViewSet, TaskViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'tasks', TaskViewSet, basename='task')
