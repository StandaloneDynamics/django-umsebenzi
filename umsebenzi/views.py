from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters import rest_framework as filters

from umsebenzi.models import Project, Task
from umsebenzi.serializers import ProjectSerializer, TaskSerializer, TaskStatusSerializer
from umsebenzi.filters import TaskFilter


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Project.objects.filter(created_by=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(created_by=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'code'
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = TaskFilter

    def get_queryset(self):
        return Task.objects.filter(Q(created_by=self.request.user) | Q(assigned_to=self.request.user))

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(created_by=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['PATCH'], serializer_class=TaskStatusSerializer)
    def status(self, request, code=None):
        task = self.get_object()
        serializer = self.get_serializer(task, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
